import unittest
from cnct import ConnectClient
from examples.connect_processor_example.connect_processor.app.purchase import Purchase
from unittest.mock import patch, MagicMock
from examples.connect_processor_example.tests.test_util import TestUtils
from examples.connect_processor_example.connect_processor.app.api_client.isv_client import APIClient


class TestPurchase(unittest.TestCase):
    # //////////////////////
    # PURCHASE UNIT TESTS
    # /////////////////////

    @patch('examples.connect_processor_example.connect_processor.app.utils.utils.Utils.update_subscription_parameters',
           MagicMock(return_value=""))
    @patch('examples.connect_processor_example.connect_processor.app.utils.utils.Utils._get_template_by_product',
           MagicMock(return_value="TL-###-###-###"))
    @patch('examples.connect_processor_example.connect_processor.app.utils.utils.Utils.approve_fulfillment_request',
           MagicMock(return_value=TestUtils.get_response("purchase_subscription_response.json")))
    @patch('examples.connect_processor_example.connect_processor.app.utils.utils.Utils.get_api_client',
           MagicMock(return_value=APIClient('http://example.org/v1')))
    @patch('examples.connect_processor_example.connect_processor.app.api_client.isv_client.APIClient.create_subscription',
           MagicMock(return_value={
                "tenantId": 123333123
            }))
    @patch('examples.connect_processor_example.connect_processor.app.api_client.isv_client.APIClient.change_subscription',
           MagicMock(return_value=''))
    def test_purchase_pass(self):
        request = TestUtils.get_response("create_purchase_request_body.json")
        response = TestUtils.get_response("purchase_subscription_response.json")
        client = ConnectClient('', '')
        result = Purchase.process_request(request, client)
        self.assertDictEqual(result, response)
