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
import json 
import copy

class SwaggerAPI(Resource):
    @swagger.doc({
        'tags': ['Get all swagger specifications'],
        'description': '',
        'responses': {
            '200': {
                'description': 'Return swagger specifications',
                'schema': UserModel,
                'examples': {
                    'application/json': {
                        'id': 1,
                        'name': 'somebody'
                    }
                }
            }
        }
    })
    def get(self):
        all_swagger = db.db["swagger"].find({})
        all_swagger_with_permission = []
        for swagger in all_swagger:
            # json load, otherwise the json string gets escaped with jsonify
            complete_swagger = json.loads(swagger.get("swagger"))
            # copy() because otherwise both variables point to the same value
            filtered_swagger = copy.deepcopy(complete_swagger)
            """
            for path in complete_swagger.get("paths"):
                if path:
                    for method in complete_swagger.get("paths")[path]:
                        if method:
                            user_has_permission = False
                            for role in json.loads(request.header.get("X-User-Roles")):
                                transformed_path = (complete_swagger.get("basePath") + path).replace("/", ":")
                                payload = {
                                    "subject": user_id,
                                    "action": method.upper(),
                                    "resource":  "endpoints" + transformed_path
                                }
                                ladon = "{url}/access".format(url=os.environ["LADON"])
                                response = requests.get(ladon, data=json.dumps(payload)).json()
                                server.app.logger.info("check for authorization at ladon: ")
                                server.app.logger.info("Request Data: " + json.dumps(payload))
                                server.app.logger.info("Response Data: " + json.dumps(response))
                                if response.get("Result"):
                                    user_has_permission = True
                                    break
                            
                            if !user_has_permission:
                                del filtered_swagger.get("paths")[path][method]
                                # TODO if no method, then delete path"""
            all_swagger_with_permission.append(filtered_swagger)
        return jsonify(all_swagger_with_permission)