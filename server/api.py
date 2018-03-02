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
        response = requests.get("http://petstore.swagger.io/v2/swagger.json").json()
        print(response)
        db.db["swagger"].insert({
            "id": "path",
            "swagger": ""
        })
        all_swagger = db.db["swagger"].find({})
        return jsonify(list(map(lambda document: document.get("swagger"), all_swagger)))