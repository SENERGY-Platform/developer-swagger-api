from unittest import TestCase, mock, main
from apis.api import transform_swagger_permission
import json


class ApiTestCase(TestCase):
    def test_transform_swagger_permission_with_empty_data(self):
        self.assertEqual(transform_swagger_permission({}, []), {})

    def test_transform_swagger_permission_with_empty_user(self):
        self.assertEqual(transform_swagger_permission(get_test_swagger(), []), get_test_swagger_filtered())

    @mock.patch('apis.util.authorization.has_access', return_value=True)
    def test_transform_swagger_permission_with_access(self, mock_has_access):
        filtered = transform_swagger_permission(get_test_swagger(), ['user'])
        mock_has_access.assert_called()
        self.assertEqual(filtered, get_test_swagger())

    @mock.patch('apis.util.authorization.has_access', return_value=False)
    def test_transform_swagger_permission_no_access(self, mock_has_access):
        actual = transform_swagger_permission(get_test_swagger(), ['user'])
        mock_has_access.assert_called()
        self.assertEqual(actual, get_test_swagger_filtered())


if __name__ == '__main__':
    main()


def get_test_swagger():
    return json.loads("{\"basePath\":\"/analytics/operator-repo/v2/\",\"consumes\":[\"application/json\"],"
                      "\"definitions\":{\"Config\":{\"properties\":{\"name\":{\"description\":\"Config name\","
                      "\"type\":\"string\"},\"type\":{\"description\":\"Config type\",\"type\":\"string\"}},"
                      "\"required\":[\"name\",\"type\"],\"type\":\"object\"},\"Input\":{\"properties\":{\"name\":{"
                      "\"description\":\"Input name\",\"type\":\"string\"},\"type\":{\"description\":\"Input type\","
                      "\"type\":\"string\"}},\"required\":[\"name\",\"type\"],\"type\":\"object\"},\"Operator\":{"
                      "\"properties\":{\"config_values\":{\"items\":{\"$ref\":\"#/definitions/Config\"},"
                      "\"type\":\"array\"},\"deploymentType\":{\"type\":\"string\"},\"description\":{"
                      "\"description\":\"Description of the operator\",\"type\":\"string\"},\"image\":{"
                      "\"description\":\"Name of the associated docker image\",\"type\":\"string\"},\"inputs\":{"
                      "\"items\":{\"$ref\":\"#/definitions/Input\"},\"type\":\"array\"},\"name\":{"
                      "\"description\":\"Operator name\",\"type\":\"string\"},\"outputs\":{\"items\":{"
                      "\"$ref\":\"#/definitions/Output\"},\"type\":\"array\"},\"pub\":{\"type\":\"boolean\"}},"
                      "\"required\":[\"name\"],\"type\":\"object\"},\"OperatorList\":{\"properties\":{\"operators\":{"
                      "\"items\":{\"$ref\":\"#/definitions/Operator\"},\"type\":\"array\"}},\"type\":\"object\"},"
                      "\"Output\":{\"properties\":{\"name\":{\"description\":\"Output name\",\"type\":\"string\"},"
                      "\"type\":{\"description\":\"Output type\",\"type\":\"string\"}},\"required\":[\"name\","
                      "\"type\"],\"type\":\"object\"}},\"host\":\"fgseitsrancher.wifa.intern.uni-leipzig.de:8000\","
                      "\"info\":{\"title\":\"Analytics Operator Repo API\",\"version\":\"0.1\","
                      "\"description\":\"Analytics Operator Repo API\"},\"paths\":{\"/doc\":{\"get\":{"
                      "\"operationId\":\"get_docs\",\"responses\":{\"200\":{\"description\":\"Success\"}},"
                      "\"tags\":[\"default\"]}},\"/operator\":{\"get\":{\"operationId\":\"get_operator\","
                      "\"parameters\":[{\"description\":\"An optional fields mask\",\"format\":\"mask\","
                      "\"in\":\"header\",\"name\":\"X-Fields\",\"type\":\"string\"}],\"responses\":{\"200\":{"
                      "\"description\":\"Success\",\"schema\":{\"$ref\":\"#/definitions/OperatorList\"}}},"
                      "\"summary\":\"Returns a list of operators\",\"tags\":[\"operator\"]},"
                      "\"put\":{\"operationId\":\"put_operator\",\"parameters\":[{\"in\":\"body\","
                      "\"name\":\"payload\",\"required\":true,\"schema\":{\"$ref\":\"#/definitions/Operator\"}},"
                      "{\"description\":\"An optional fields mask\",\"format\":\"mask\",\"in\":\"header\","
                      "\"name\":\"X-Fields\",\"type\":\"string\"}],\"responses\":{\"201\":{"
                      "\"description\":\"Success\",\"schema\":{\"$ref\":\"#/definitions/Operator\"}}},"
                      "\"summary\":\"Creates a operator\",\"tags\":[\"operator\"]}},\"/operator/{operator_id}\":{"
                      "\"delete\":{\"operationId\":\"delete_operator_update\",\"responses\":{\"204\":{"
                      "\"description\":\"Deleted\"},\"404\":{\"description\":\"Operator not found.\"}},"
                      "\"summary\":\"Deletes a operator\",\"tags\":[\"operator\"]},\"get\":{"
                      "\"operationId\":\"get_operator_update\",\"parameters\":[{\"description\":\"An optional fields "
                      "mask\",\"format\":\"mask\",\"in\":\"header\",\"name\":\"X-Fields\",\"type\":\"string\"}],"
                      "\"responses\":{\"200\":{\"description\":\"Success\",\"schema\":{"
                      "\"$ref\":\"#/definitions/Operator\"}},\"404\":{\"description\":\"Operator not found.\"}},"
                      "\"summary\":\"Get a operator\",\"tags\":[\"operator\"]},\"parameters\":[{\"in\":\"path\","
                      "\"name\":\"operator_id\",\"required\":true,\"type\":\"string\"}],\"post\":{"
                      "\"operationId\":\"post_operator_update\",\"parameters\":[{\"in\":\"body\","
                      "\"name\":\"payload\",\"required\":true,\"schema\":{\"$ref\":\"#/definitions/Operator\"}},"
                      "{\"description\":\"An optional fields mask\",\"format\":\"mask\",\"in\":\"header\","
                      "\"name\":\"X-Fields\",\"type\":\"string\"}],\"responses\":{\"200\":{"
                      "\"description\":\"Success\",\"schema\":{\"$ref\":\"#/definitions/Operator\"}},"
                      "\"404\":{\"description\":\"Operator not found.\"}},\"summary\":\"Updates a operator\","
                      "\"tags\":[\"operator\"]}}},\"produces\":[\"application/json\"],\"responses\":{\"MaskError\":{"
                      "\"description\":\"When any error occurs on mask\"},\"ParseError\":{\"description\":\"When a "
                      "mask can't be parsed\"}},\"schemes\":[\"https\",\"http\"],\"swagger\":\"2.0\",\"tags\":[{"
                      "\"description\":\"Default namespace\",\"name\":\"default\"},{\"description\":\"Operations "
                      "related to operators\",\"name\":\"operator\"}]}")

def get_test_swagger_filtered():
    return json.loads("{\"basePath\":\"/analytics/operator-repo/v2/\",\"consumes\":[\"application/json\"],"
                      "\"definitions\":{\"Config\":{\"properties\":{\"name\":{\"description\":\"Config name\","
                      "\"type\":\"string\"},\"type\":{\"description\":\"Config type\",\"type\":\"string\"}},"
                      "\"required\":[\"name\",\"type\"],\"type\":\"object\"},\"Input\":{\"properties\":{\"name\":{"
                      "\"description\":\"Input name\",\"type\":\"string\"},\"type\":{\"description\":\"Input type\","
                      "\"type\":\"string\"}},\"required\":[\"name\",\"type\"],\"type\":\"object\"},\"Operator\":{"
                      "\"properties\":{\"config_values\":{\"items\":{\"$ref\":\"#/definitions/Config\"},"
                      "\"type\":\"array\"},\"deploymentType\":{\"type\":\"string\"},\"description\":{"
                      "\"description\":\"Description of the operator\",\"type\":\"string\"},\"image\":{"
                      "\"description\":\"Name of the associated docker image\",\"type\":\"string\"},\"inputs\":{"
                      "\"items\":{\"$ref\":\"#/definitions/Input\"},\"type\":\"array\"},\"name\":{"
                      "\"description\":\"Operator name\",\"type\":\"string\"},\"outputs\":{\"items\":{"
                      "\"$ref\":\"#/definitions/Output\"},\"type\":\"array\"},\"pub\":{\"type\":\"boolean\"}},"
                      "\"required\":[\"name\"],\"type\":\"object\"},\"OperatorList\":{\"properties\":{\"operators\":{"
                      "\"items\":{\"$ref\":\"#/definitions/Operator\"},\"type\":\"array\"}},\"type\":\"object\"},"
                      "\"Output\":{\"properties\":{\"name\":{\"description\":\"Output name\",\"type\":\"string\"},"
                      "\"type\":{\"description\":\"Output type\",\"type\":\"string\"}},\"required\":[\"name\","
                      "\"type\"],\"type\":\"object\"}},\"host\":\"fgseitsrancher.wifa.intern.uni-leipzig.de:8000\","
                      "\"info\":{\"title\":\"Analytics Operator Repo API\",\"version\":\"0.1\","
                      "\"description\":\"Analytics Operator Repo API\"},\"paths\":{\"/doc\":{},\"/operator\":{},"
                      "\"/operator/{operator_id}\":{}},\"produces\":[\"application/json\"],\"responses\":{"
                      "\"MaskError\":{\"description\":\"When any error occurs on mask\"},\"ParseError\":{"
                      "\"description\":\"When a mask can't be parsed\"}},\"schemes\":[\"https\",\"http\"],"
                      "\"swagger\":\"2.0\",\"tags\":[{\"description\":\"Default namespace\",\"name\":\"default\"},"
                      "{\"description\":\"Operations related to operators\",\"name\":\"operator\"}]}")
