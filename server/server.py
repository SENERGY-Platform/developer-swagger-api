from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_restful import Api
import db 
from flask_migrate import Migrate
import api 
import logging
from time import strftime
import traceback
from datetime import datetime
from threading import Timer
import requests
import base64
from requests.auth import HTTPBasicAuth
import yaml
import json

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)
app_api = Api(app)
app_api.add_resource(api.SwaggerAPI, '/developer/swagger')

@app.after_request
def after_request(response):
    # This IF avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
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

def get_swagger_files_from_repos_timer():
    x=datetime.today()
    y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds+1
    t = Timer(secs, get_swagger_files_from_repos)
    t.start()

def get_swagger_files_from_repos():
    try:
        db.db["swagger"].remove({})
        all_projects = []
        response = requests.get("https://gitlab.wifa.uni-leipzig.de/api/v4/projects?private_token=" + os.environ["TOKEN"])
        all_projects = all_projects + response.json()
        next_page = response.headers["X-Page"] != response.headers["X-Total-Pages"]
        while next_page:
            response = requests.get("https://gitlab.wifa.uni-leipzig.de/api/v4/projects?private_token=" + os.environ["TOKEN"] + "&page=" + response.headers["X-Next-Page"])
            all_projects = all_projects + response.json()
            next_page = response.headers["X-Page"] != response.headers["X-Total-Pages"]
        
        for project in all_projects:
            app.logger.info("check project " + project.get("name"))
            url = "https://gitlab.wifa.uni-leipzig.de/api/v4/projects/" + str(project.get("id")) + "/repository/files/swagger.yaml/raw?ref=master&private_token=" + os.environ["TOKEN"]
            request = requests.Request("GET", url)
            prepared = request.prepare()
            prepared.url = prepared.url.replace("swagger.yaml", "swagger%2Eyaml")
            session = requests.Session()
            response = session.send(prepared)
            if response.status_code == 200:
                db.db["swagger"].insert({
                    "swagger": json.dumps(yaml.load(response.text))
                })
                app.logger.info("inserted swagger file of gitlab repo " + str(project.get("name")))

        # TODO env variable
        kong_apis = requests.get("http://kong.kong.rancher.internal:8001/apis", auth=HTTPBasicAuth('sepl', 'sepl')).json()
        app.logger.info(kong_apis)
 
        for api in kong_apis.get("data"):
            try:
                app.logger.info(json.dumps(api))
                response = requests.get(api.get("upstream_url") + "/doc") # + api.get("uris")[0] not needed because apis get stripped 
                if response.status_code == 200:
                    db.db["swagger"].insert({
                        "swagger": response.text
                    })
                    app.logger.info("inserted swagger file from documentation endpoint of service " + api.get("name"))
            except Exception as e:
                app.logger.error(e)
                continue
                
    except Exception as e:
        app.logger.error(e)

get_swagger_files_from_repos()
get_swagger_files_from_repos_timer()

if __name__ == '__main__':
    if os.environ["DEBUG"] == "true":
        app.run(debug=True,host='0.0.0.0')
    else:
        app.run(debug=False, host='0.0.0.0')