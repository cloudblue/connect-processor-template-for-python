import unittest

from cnct import ConnectClient
from connect_processor.app.dynamic_validation import do_validate
from unittest.mock import patch, MagicMock
from test_util import TestUtils

config_file = TestUtils.get_config_file()
# apiEndpoint is the API End-point of Connect
connect_api_url = config_file['connectApiEndpoint']
# apiKey is the API key for authorization created in Integrations menu of Connect
connect_key = config_file['connectApiKey']
# products are the list of IDs of the products which needs to be processed by this Processor
# client = ConnectClient(api_key=connect_key[0], endpoint=connect_api_url[0])
client = ''

class TestDynamicValidation(unittest.TestCase):
    # //////////////////////
    # DYNAMIC VALIDATION UNIT TESTS
    # /////////////////////

    @patch('connect_processor.app.dynamic_validation.get_validation_request_data',
           MagicMock(return_value=TestUtils.get_response("dynamic_validation_request.json")))

    def test_dynamic_validation_pass(self):

        response = TestUtils.get_response("dynamic_validation_request.json")
        result = do_validate()
        self.assertDictEqual(result.get_json(), response)
