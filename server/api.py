import schemas 
import models
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
        """
        parser = ResolvingParser('path/to/my/swagger.yaml')
        """
        response = requests.get("http://petstore.swagger.io/v2/swagger.json").json()
        db.db.insert_one(response)