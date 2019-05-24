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

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)
app_api = Api(app, api_version='0.0', api_spec_url='/doc', host='0.0.0.0:8088')
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
            response = requests.get(api.get("upstream_url") + "/doc") # + api.get("uris")[0] not needed because apis get stripped 
            if response.status_code == 200:
                try: 
                    json.loads(response.text)
                    db.db["swagger"].insert({
                        "swagger": response.text
                    })
                except ValueError as e:
                    app.logger.info("document from /doc endpoint is not json, therefore dont get loaded")
            app.logger.info("inserted swagger file from documentation endpoint of service " + api.get("name"))
        except Exception as e:
            app.logger.error(e)
            continue

def getApisFromKong():
    response = requests.get(os.environ["KONG_INTERNAL_URL"], auth=HTTPBasicAuth(os.environ["KONG_INTERNAL_BASIC_USER"], os.environ["KONG_INTERNAL_BASIC_PW"]))
    return response.json().get("data")

load_doc()

if __name__ == '__main__':
    if os.environ["DEBUG"] == "true":
        app.run(debug=True,host='0.0.0.0')
    else:
        app.run(debug=False, host='0.0.0.0')
