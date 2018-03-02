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
"""
x=datetime.today()
y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def update_swagger_files():
    http://gitlab.wifa.uni-leipzig.de/api/v4/projects?private_token=" + os.environ["TOKEN"]

t = Timer(secs, hello_world)
t.start()
"""

if __name__ == '__main__':
    if os.environ["DEBUG"] == "true":
        app.run(debug=True,host='0.0.0.0')
    else:
        app.run(debug=False, host='0.0.0.0')