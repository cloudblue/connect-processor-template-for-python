import unittest

from cnct import ConnectClient
from connect_processor.app.purchase import Purchase
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


class TestPurchase(unittest.TestCase):
    # //////////////////////
    # PURCHASE UNIT TESTS
    # /////////////////////

    @patch('connect_processor.app.utils.utils.Utils.update_subscription_parameters',
           MagicMock(return_value=""))
    @patch('connect_processor.app.utils.utils.Utils._get_template_by_product',
           MagicMock(return_value="TL-###-###-###"))
    @patch('connect_processor.app.utils.utils.Utils.approve_fulfillment_request',
           MagicMock(return_value=TestUtils.get_response("purchase_subscription_response.json")))
    def test_purchase_pass(self):
        request = TestUtils.get_response("create_purchase_request_body.json")
        response = TestUtils.get_response("purchase_subscription_response.json")
        result = Purchase.process_request(request, client)
        self.assertDictEqual(result, response)
