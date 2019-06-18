from flask import Flask,request
import os
import db
import api
import logging
from time import strftime
import requests
from requests.auth import HTTPBasicAuth
import json
from flask_restful_swagger_2 import Api
from threading import Timer

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)
app_api = Api(app, api_version='0.0', api_spec_url='/doc')
app_api.add_resource(api.SwaggerAPI, '/')

@app.after_request
def after_request(response):
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        app.logger.info('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      request.data
                      )
    return response



def load_doc():
    db.db["swagger"].remove({})
    kong_apis = getApisFromKong()
    app.logger.info(kong_apis)
 
    for api in kong_apis:
        try:
            app.logger.info(json.dumps(api))
            response = requests.get(os.environ['KONG_HOST']+api.get("paths")[0] + "/doc") # + api.get("uris")[0] not needed because apis get stripped
            if response.status_code == 200:
                try:
                    #if entry contains empty basepath, replace with basePath from Kong
                    definition = response.text.replace("\"basePath\": \"/\"", "\"basePath\": \""+api.get("paths")[0]+"/\"")
                    if definition.find('host') == -1:
                        #if entry contains no host, set KONG_HOST
                        definition = definition.replace("\"swagger\": \"2.0\",", "\"swagger\": \"2.0\",\n\"host\": \""+os.environ['KONG_HOST']+"\",")
                    if definition.find('schemes') == -1:
                        #if entry containes no schemes, add http/https
                        definition = definition.replace("\"swagger\": \"2.0\",", "\"swagger\": \"2.0\",\n\"schemes\": [\"https\", \"http\"],")
                    json.loads(definition)
                    db.db["swagger"].insert({
                        "swagger": definition
                    })
                    app.logger.info("inserted swagger file from documentation endpoint of service " + api.get("paths")[0])
                except ValueError as e:
                    app.logger.info("document from" + api.get("paths")[0] +" /doc endpoint is not json, therefore dont get loaded")
            else:
                app.logger.info(api.get("name") + " responded with " + str(response.status_code) + ". No documentation added.")
        except Exception as e:
            app.logger.error(e)
            continue
    Timer(3600.0, load_doc).start()    #reruns function every hour

def getApisFromKong():
    try:
        user = os.environ["KONG_INTERNAL_BASIC_USER"]
        pw = os.environ["KONG_INTERNAL_BASIC_PW"]
        response = requests.get(os.environ["KONG_INTERNAL_URL"], auth=HTTPBasicAuth(user, pw))
    except KeyError:
        print('Could not load user or password from environment variables. Attempting to contact Kong without BasicAuth.')
        response = requests.get(os.environ["KONG_INTERNAL_URL"])
    return response.json().get("data")

load_doc()

if __name__ == '__main__':
    if os.environ["DEBUG"] == "true":
        app.run(debug=True,host='0.0.0.0')
    else:
        app.run(debug=False, host='0.0.0.0')
