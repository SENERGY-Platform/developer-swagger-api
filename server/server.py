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
        all_projects = []
        response = requests.get("http://gitlab.wifa.uni-leipzig.de/api/v4/projects?private_token=" + os.environ["TOKEN"])
        all_projects = all_projects + response.json()
        next_page = response.headers["X-Page"] != response.headers["X-Total-Pages"]
        while next_page:
            response = requests.get("http://gitlab.wifa.uni-leipzig.de/api/v4/projects?private_token=" + os.environ["TOKEN"] + "&page=" + response.headers["X-Next-Page"])
            all_projects = all_projects + response.json()
            next_page = response.headers["X-Page"] != response.headers["X-Total-Pages"]
        
        for project in all_projects:
            app.logger.info("check project " + project.get("name"))
            swagger_file = requests.get("http://gitlab.wifa.uni-leipzig.de/api/v4/projects/" + str(project.get("id")) + "/repository/files/swagger%2Eyaml/raw?ref=master&private_token=" + os.environ["TOKEN"])
            app.logger.info(swagger_file.status_code)
            if swagger_file.status_code == 200:
                db.db["swagger"].insert({
                    "id": project.get("id"),
                    "swagger": swagger_file.text
                })
                app.logger.info("inserted swagger file of repo " + project.get("id"))
    except Exception as e:
        app.logger.error(e)


if __name__ == '__main__':
    if os.environ["DEBUG"] == "true":
        app.run(debug=True,host='0.0.0.0')
    else:
        app.run(debug=False, host='0.0.0.0')