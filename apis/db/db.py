from pymongo import MongoClient
import os
import apis.util.kong as kong
import requests
from threading import Timer
import json
import logging

logger = logging.getLogger("apis.db.db")

if "DB_HOST" not in os.environ or "DB_HOST" == "" or "DB_PORT" not in os.environ or "DB_PORT" == "":
    logger.error("DB_HOST and/or DB_PORT not set")
else:
    client = MongoClient('mongodb://{host}:{port}/'.format(host=os.environ["DB_HOST"], port=os.environ["DB_PORT"]))
    db = client.swagger


def load_doc():
    kong_routes = kong.get_routes_from_kong()
    kong_services = kong.get_services_from_kong()
    logging.info(kong_routes)

    for route in kong_routes:
        try:
            logging.info(json.dumps(route))
            logging.info("Trying to get doc from " + str(route.get("paths")[0]))
            upstream_service = kong.get_upstream(kong_services, route.get("service").get("id"))
            upstream_url = upstream_service.get("protocol") + "://" + upstream_service.get("host") + ":" + str(
                upstream_service.get("port")) + "/doc"
            logging.info("Upstream URL is " + upstream_url)
            response = requests.get(upstream_url, timeout=1)
            logging.info("Got response with code " + str(response.status_code))
            if response.status_code == 200:
                try:
                    # if entry contains empty basepath, replace with basePath from Kong
                    logging.info("Setting basePath if not set")
                    definition = response.text.replace("\"basePath\": \"/\"",
                                                       "\"basePath\": \"" + str(route.get("paths")[0]) + "/\"")
                    if definition.find('host') == -1:
                        logging.info("Did not find host entry, setting to " + os.environ['KONG_HOST'])
                        # if entry contains no host, set KONG_HOST
                        definition = definition.replace("\"swagger\": \"2.0\",",
                                                        "\"swagger\": \"2.0\",\n\"host\": \"" + os.environ[
                                                            'KONG_HOST'] + "\",")
                    if definition.find('schemes') == -1:
                        logging.info("Did not find schemes entry, setting to [https,http]")
                        # if entry containes no schemes, add http/https
                        definition = definition.replace("\"swagger\": \"2.0\",",
                                                        "\"swagger\": \"2.0\",\n\"schemes\": [\"https\", \"http\"],")
                    json.loads(definition)
                    db.db["swagger"].remove({})
                    db.db["swagger"].insert({
                        "swagger": definition
                    })
                    logging.info(
                        "inserted swagger file from documentation endpoint of service " + str(route.get("paths")[0]))
                except ValueError as e:
                    logging.info("document from" + str(
                        route.get("paths")[0]) + " /doc endpoint is not json, therefore dont get loaded")
            else:
                logging.info(str(route.get("paths")[0]) + " responded with " + str(
                    response.status_code) + ". No documentation added.")
        except Exception as e:
            logging.error(e)
            continue
    Timer(3600.0, load_doc).start()  # reruns function every hour


def get_swagger_files():
    return db["swagger"].find({})
