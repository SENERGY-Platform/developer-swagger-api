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
            return jsonify([json.loads(swagger.get("swagger")) for swagger in all_swagger])
        else:
            for swagger in all_swagger:
                # json load, otherwise the json string gets escaped with jsonify
                complete_swagger = None
                try:
                    complete_swagger = json.loads(swagger.get("swagger"))
                except Exception as e:
                    server.app.logger.info(swagger.get("swagger"))
                    server.app.logger.error(e)

                if complete_swagger:
                    filtered_swagger = []
                    server.app.logger.info(complete_swagger)
                    # Check if API is public accessible
                    if complete_swagger.get("host") == "api.sepl.infai.org": 
                        for api in public_apis:
                            server.app.logger.info(complete_swagger.get("basePath"))
                            server.app.logger.info(api.get("uris")[0])
                            if complete_swagger.get("basePath") == api.get("uris")[0]:
                                transformed_swagger = transform_swagger_permission(complete_swagger, roles)
                                filtered_swagger.append(transformed_swagger)
                    else:
                        # APIs is not in KONG, therefor accessible
                        transformed_swagger = transform_swagger_permission(complete_swagger, ["admin"])
                        filtered_swagger.append(transformed_swagger)
            return jsonify(filtered_swagger)


