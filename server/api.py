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

class AllSwaggerAPI(Resource):
    def get(self):
        all_swagger = db.db["swagger"].find({})
        all_swagger_with_permission = []
        for swagger in all_swagger:
            complete_swagger = json.loads(swagger.get("swagger"))
            all_swagger_with_permission.append(complete_swagger)
        return jsonify(all_swagger_with_permission)

class PublicSwaggerAPI(Resource):
    def get(self):
        all_swagger = db.db["swagger"].find({})
        all_swagger_with_permission = []
        public_apis = server.getApisFromKong()
        for swagger in all_swagger:
            # json load, otherwise the json string gets escaped with jsonify
            complete_swagger = json.loads(swagger.get("swagger"))
            if complete_swagger.get("host") == "api.sepl.infai.org":
                for api in public_apis:
                    if complete_swagger.get("basePath") == api.get("uris")[0]:
                        all_swagger_with_permission.append(complete_swagger)
            else:
                all_swagger_with_permission.append(complete_swagger)

        return jsonify(all_swagger_with_permission)
"""
filter with roles
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
                                # TODO if no method, then delete path
"""