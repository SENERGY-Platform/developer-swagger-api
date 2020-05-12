import os
import requests
from requests.auth import HTTPBasicAuth


def getRoutesFromKong():
    try:
        user = os.environ["KONG_INTERNAL_BASIC_USER"]
        pw = os.environ["KONG_INTERNAL_BASIC_PW"]
        response = requests.get(os.environ["KONG_INTERNAL_URL"] + "/routes", auth=HTTPBasicAuth(user, pw))
    except KeyError:
        print(
            'Could not load user or password from environment variables. Attempting to contact Kong without BasicAuth.')
        response = requests.get(os.environ["KONG_INTERNAL_URL"] + "/routes")
    return response.json().get("data")


def getServicesFromKong():
    try:
        user = os.environ["KONG_INTERNAL_BASIC_USER"]
        pw = os.environ["KONG_INTERNAL_BASIC_PW"]
        response = requests.get(os.environ["KONG_INTERNAL_URL"] + "/services", auth=HTTPBasicAuth(user, pw))
    except KeyError:
        print(
            'Could not load user or password from environment variables. Attempting to contact Kong without BasicAuth.')
        response = requests.get(os.environ["KONG_INTERNAL_URL"] + "/services")
    return response.json().get("data")


def getUpstream(services, id):
    for service in services:
        if service.get('id') == id:
            return service
    raise Exception('Could not find service for id ' + id)
