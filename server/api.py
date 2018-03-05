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
        # TODO: compare with ladon with role path and method, new header field 
        payload = {
            "subject": "role",
            "action": "method",
            "resource": "path"
        }
        #response = requests.get(os.environ["LADON"], payload=payload).json()
        return jsonify(list(map(lambda document: document.get("swagger"), all_swagger)))