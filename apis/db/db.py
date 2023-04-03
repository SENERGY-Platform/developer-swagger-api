from pymongo import MongoClient
import os

from pymongo.collection import Collection
from pymongo.database import Database

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
    db = Database(client, "swagger")
    collection = Collection(db, "swagger")


def load_doc():
    kong_routes = kong.get_routes_from_kong()
    kong_services = kong.get_services_from_kong()
    logging.info(kong_routes)

    for route in kong_routes:
        try:
            logging.info(json.dumps(route))
            path = str(route.get("paths")[0])
            logging.info("Trying to get doc from " + path)
            upstream_service = kong.get_upstream(kong_services, route.get("service").get("id"))
            upstream_url = upstream_service.get("protocol") + "://" + upstream_service.get("host") + ":" + str(
                upstream_service.get("port")) + "/doc"
            logging.info("Upstream URL is " + upstream_url)
            response = requests.get(upstream_url, timeout=1)
            logging.info("Got response with code " + str(response.status_code))
            if response.status_code == 200:
                swagger_definition = json.loads(response.text)
                logging.debug("Length is " + str(len(response.text)))
                try:
                    swagger_definition['basePath'] = path
                    swagger_definition['host'] = os.environ['KONG_HOST'] + ":" + os.environ['KONG_PORT']
                    
                    # if entry containes no schemes, add http/https
                    if 'schemes' not in swagger_definition:
                        logging.info("Did not find schemes entry, setting to [https]")
                        swagger_definition['schemes'] = ['https']

                    collection.replace_one({"path": path}, {"path": path, "swagger": json.dumps(swagger_definition)}, upsert=True)
                    logging.info(
                        "inserted swagger file from documentation endpoint of service " + path)
                except ValueError as e:
                    logging.info(str(e))
            else:
                logging.info(str(route.get("paths")[0]) + " responded with " + str(
                    response.status_code) + ". No documentation added.")
        except Exception as e:
            logging.error(e)
            continue
    Timer(3600.0, load_doc).start()  # reruns function every hour


def get_swagger_files():
    return collection.find({})
