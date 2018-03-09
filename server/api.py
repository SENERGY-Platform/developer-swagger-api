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
    def get(self):
        user_id = request.headers.get("X-UserID")
        all_swagger = db.db["swagger"].find({})
        all_swagger_with_permission = []
        for swagger in all_swagger:
            # json load, otherwise the json string gets escaped with jsonify
            complete_swagger = json.loads(swagger.get("swagger"))
            # copy() because otherwise both variables point to the same value
            filtered_swagger = copy.deepcopy(complete_swagger)

            for path in complete_swagger.get("paths"):
                server.app.logger.info(json.dumps(path))
                if path:
                    for method in complete_swagger.get("paths")[path]:
                        server.app.logger.info(json.dumps(method))
                        if method:
                            payload = {
                                "subject": user_id,
                                "action": method.upper(),
                                "resource": path
                            }
                            ladon = "{url}/access".format(url=os.environ["LADON"])
                            response = requests.get(ladon, data=json.dumps(payload)).json()
                            if not response.get("Result"):
                                del filtered_swagger.get("paths")[path][method]
                                # TODO if no method, then delete path
            all_swagger_with_permission.append(filtered_swagger)
        return jsonify(all_swagger_with_permission)