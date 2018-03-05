import schemas 
import db
import json
import requests
from flask import request, jsonify
from flask_restful import Resource
import os 
import server
import logging
from prance import ResolvingParser

class SwaggerAPI(Resource):
    def get(self):
        all_swagger = db.db["swagger"].find({})
        all_swagger_with_permission = []
        for swagger in all_swagger:
            all_swagger_with_permission.append(swagger.get("swagger"))
            server.app.logger.info(swagger)
        # TODO: compare with ladon with role path and method, new header field 
        payload = {
            "subject": "role",
            "action": "method",
            "resource": "path"
        }
        #response = requests.get(os.environ["LADON"], payload=payload).json()
        return jsonify(all_swagger_with_permission)