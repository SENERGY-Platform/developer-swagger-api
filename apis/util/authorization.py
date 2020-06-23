import logging
import requests
import json
import os


def has_access(subject: str, path: str, action: str) -> bool:
    logger = logging.getLogger("apis.util.authorization")
    if "LADON_URL" not in os.environ or os.environ["LADON_URL"] == "":
        logger.error("LADON_URL not set")
        return False

    transformed_path = path.replace("/", ":")
    payload = {
        "subject": subject,
        "action": action,
        "resource": "endpoints" + transformed_path
    }
    ladon = "{url}/access".format(url=os.environ["LADON_URL"])
    response = requests.get(ladon, data=json.dumps(payload))
    logger.debug("check for authorization at ladon")
    logger.debug("Request Data: " + json.dumps(payload))

    if not response.ok:
        logger.error("received non OK status code from ladon, code: " + str(response.status_code))
        return False

    try:
        response_json = response.json()
    except ValueError:
        logger.error("ladon provided invalid response")
        return False

    logger.debug("Response Data: " + str(response_json))

    has_access = response_json.get("result", False)
    if not isinstance(has_access, bool):
        logger.error("ladon provided non-boolean answer")
        return False
    return has_access
