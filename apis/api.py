import copy
import json
import logging
import os

import jwt
from flask import request, jsonify
from flask_restx import Resource, Namespace, abort

import apis.util.authorization as authorization
import apis.util.kong as kong
from apis.db import db

api = Namespace("swagger")
logger = logging.getLogger("apis.api")


def transform_swagger_permission(swagger, roles):
    filtered_swagger = copy.deepcopy(swagger)
    # Remove Methods and path were the role has no permissions
    if "paths" not in swagger:
        logger.warning("transform_swagger_permission called with invalid swagger object")
        return filtered_swagger
    for path in swagger.get("paths"):
        if path:
            for method in swagger.get("paths")[path]:
                if method:
                    user_has_permission = False
                    for role in roles:
                        if authorization.has_access(role, swagger.get("basePath") + path, method.upper()):
                            user_has_permission = True
                            break

                    if not user_has_permission:
                        del filtered_swagger.get("paths")[path][method]
    return filtered_swagger


@api.route('')
class SwaggerAPI(Resource):
    def get(self):
        try:
            token = jwt.decode(request.headers.get("Authorization").split(" ")[1], verify=False)
        except Exception:
            abort(401)
        roles = token.get("realm_access")
        if roles:
            roles = roles.get("roles")

        all_swagger = db.db["swagger"].find({})
        if "admin" in roles:
            logging.info("user role is admin -> return all")
            return jsonify([json.loads(swagger.get("swagger")) for swagger in all_swagger])
        else:
            logging.info(
                "user role is not admin -> remove paths from swagger where user role does not have access")
            filtered_swagger = []
            for swagger in all_swagger:
                # json load, otherwise the json string gets escaped with jsonify
                complete_swagger = None
                try:
                    complete_swagger = json.loads(swagger.get("swagger"))
                except ValueError as e:
                    logging.info(e)

                if complete_swagger:
                    logging.info("swagger file was parsed to json")
                    # Check if API is public accessible
                    if complete_swagger.get("host") == os.environ["KONG_HOST"]:
                        transformed_swagger = transform_swagger_permission(complete_swagger, roles)
                        filtered_swagger.append(transformed_swagger)
                    else:
                        # APIs is not in KONG, therefor accessible
                        transformed_swagger = transform_swagger_permission(complete_swagger, ["admin"])
                        filtered_swagger.append(transformed_swagger)
            return jsonify(filtered_swagger)
