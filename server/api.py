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
import jwt

def transform_swagger_permission(swagger, roles):
    filtered_swagger = copy.deepcopy(swagger)
    # Remove Methods and path were the role has no permissions
    for path in swagger.get("paths"):
        if path:
            for method in swagger.get("paths")[path]:
                if method:
                    user_has_permission = False
                    for role in roles:
                        transformed_path = (swagger.get("basePath") + path).replace("/", ":")
                        payload = {
                            "subject": role,
                            "action": method.upper(),
                            "resource":  "endpoints" + transformed_path
                        }
                        ladon = "{url}/access".format(url=os.environ["LADON_URL"])
                        response = requests.get(ladon, data=json.dumps(payload)).json()
                        server.app.logger.info("check for authorization at ladon: ")
                        server.app.logger.info("Request Data: " + json.dumps(payload))
                        server.app.logger.info("Response Data: " + json.dumps(response))
                        if response.get("Result"):
                            user_has_permission = True
                            break
                                    
                    if not user_has_permission:
                        del filtered_swagger.get("paths")[path][method]
    return filtered_swagger
            

class SwaggerAPI(Resource):
    def get(self):
        token = jwt.decode(request.headers.get("Authorization").split(" ")[1], verify=False)
        roles = token.get("realm_access")
        if roles:
            roles = roles.get("roles")

        all_swagger = db.db["swagger"].find({})
        public_apis = server.getApisFromKong()
        if "admin" in roles:
            server.app.logger.info("user role is admin -> return all")
            return jsonify([json.loads(swagger.get("swagger")) for swagger in all_swagger])
        else:
            server.app.logger.info("user role is not admin -> remove paths from swagger where user role does not have access")
            filtered_swagger = []
            for swagger in all_swagger:
                # json load, otherwise the json string gets escaped with jsonify
                complete_swagger = None
                try:
                    complete_swagger = json.loads(swagger.get("swagger"))
                except ValueError as e:
                    server.app.logger.info(e)

                if complete_swagger:
                    server.app.logger.info("swagger file was parsed to json")
                    # Check if API is public accessible
                    if complete_swagger.get("host") == "api.sepl.infai.org": 
                        for api in public_apis:
                            if complete_swagger.get("basePath") == api.get("uris")[0]:
                                transformed_swagger = transform_swagger_permission(complete_swagger, roles)
                                filtered_swagger.append(transformed_swagger)
                    else:
                        # APIs is not in KONG, therefor accessible
                        transformed_swagger = transform_swagger_permission(complete_swagger, ["admin"])
                        filtered_swagger.append(transformed_swagger)
            return jsonify(filtered_swagger)


