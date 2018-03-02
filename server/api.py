import schemas 
import db
import json
import requests
from flask import request
from flask_restful import Resource
import os 
import server
import logging
from prance import ResolvingParser

class SwaggerAPI(Resource):
    def get(self):
        response = requests.get("http://petstore.swagger.io/v2/swagger.json").json()
        db.db.swagger.insert(response)
        cursor = db.db.find({})
        for document in cursor:
            print(document)