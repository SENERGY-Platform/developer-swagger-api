import os
import apis.db.db as db

import logging
from time import strftime

from flask import Flask, request
from flask_restx import Api, Resource

import apis.api as swagger_api


application = Flask(__name__)
application.logger.addHandler(logging.StreamHandler())
application.logger.setLevel(logging.INFO)
app_api = Api(application, api_version='0.0')
app_api.add_namespace(swagger_api.api)

@app_api.route('/doc')
class Docs(Resource):
    def __init__(self, kwargs):
        super().__init__(kwargs)

    def get(self):
        return app_api.__schema__

@application.after_request
def after_request(response):
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        application.logger.info('%s %s %s %s %s %s',
                                ts,
                                request.remote_addr,
                                request.method,
                                request.scheme,
                                request.full_path,
                                request.data
                                )
    return response

db.load_doc()

if __name__ == '__main__':
    if os.environ["DEBUG"] == "true":
        application.run(debug=True,host='0.0.0.0')
    else:
        application.run(debug=False, host='0.0.0.0')
