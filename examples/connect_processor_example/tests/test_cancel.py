import unittest
from cnct import ConnectClient
from examples.connect_processor_example.connect_processor.app.cancel import Cancel
from unittest.mock import patch, MagicMock
from examples.connect_processor_example.tests.test_util import TestUtils
from examples.connect_processor_example.connect_processor.app.api_client.isv_client import APIClient


class TestCancel(unittest.TestCase):
    # //////////////////////
    # CANCEL UNIT TESTS
    # /////////////////////

    @patch('examples.connect_processor_example.connect_processor.app.utils.utils.Utils.approve_fulfillment_request',
           MagicMock(return_value=TestUtils.get_response("purchase_subscription_response.json")))
    @patch('examples.connect_processor_example.connect_processor.app.utils.utils.Utils._get_template_by_product',
           MagicMock(return_value="TL-###-###-###"))
    @patch('examples.connect_processor_example.connect_processor.app.utils.utils.Utils.get_api_client',
           MagicMock(return_value=APIClient('http://example.org/v1')))
    @patch('examples.connect_processor_example.connect_processor.app.api_client.isv_client.APIClient.cancel_subscription',
           MagicMock(return_value=''))
    def test_cancel_pass(self):
        request = TestUtils.get_response("create_purchase_request_body.json")
        response = TestUtils.get_response("purchase_subscription_response.json")
        client = ConnectClient('', '')
        result = Cancel.process_request(request, client)
        self.assertDictEqual(result, response)
