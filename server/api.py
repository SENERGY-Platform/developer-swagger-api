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
            "path": "1"
        })
        cursor = db.db["swagger"].find({})
        print(cursor)
        for document in cursor:
            print(document)

        return jsonify([])