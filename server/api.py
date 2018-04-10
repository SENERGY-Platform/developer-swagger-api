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

class SwaggerAPI(Resource):
    def get(self):
        server.app.logger.info(request.headers.get("Authorization"))
        roles = jwt.decode(request.headers.get("Authorization").split(" ")[1], verify=False)
        server.app.logger.info(roles)
        all_swagger = db.db["swagger"].find({})
        all_swagger_with_permission = []
        public_apis = server.getApisFromKong()
        for swagger in all_swagger:
            # json load, otherwise the json string gets escaped with jsonify
            complete_swagger = json.loads(swagger.get("swagger"))
            if role == "admin":
                all_swagger_with_permission.append(complete_swagger)
            else:
                # Check if API is public accessible
                if complete_swagger.get("host") == "api.sepl.infai.org":
                    # 
                    for api in public_apis:
                        if complete_swagger.get("basePath") == api.get("uris")[0]:
                            all_swagger_with_permission.append(complete_swagger)
                else:
                    # APIs is not in KONG, therefor accessible
                    all_swagger_with_permission.append(complete_swagger)

                # Remove Methods and path were the role has no permissions
                for path in complete_swagger.get("paths"):
                    if path:
                        for method in complete_swagger.get("paths")[path]:
                            if method:
                                user_has_permission = False
                                for role in roles:
                                    transformed_path = (complete_swagger.get("basePath") + path).replace("/", ":")
                                    payload = {
                                        "subject": user_id,
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

        return jsonify(all_swagger_with_permission)
