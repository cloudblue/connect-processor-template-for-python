import unittest

from cnct import ConnectClient
from connect_processor.app.purchase import Purchase
from unittest.mock import patch, MagicMock

from tests.test_util import TestUtils

project_manager = __import__('connect_processor.app', globals(), locals(),
                                 ['purchase', 'change', 'cancel', 'suspend', 'resume'], 0)

config_file = TestUtils.get_config_file()
# apiEndpoint is the API End-point of Connect
connect_api_url = config_file['connectApiEndpoint'],
# apiKey is the API key for authorization created in Integrations menu of Connect
connect_key = config_file['connectApiKey'],
# products are the list of IDs of the products which needs to be processed by this Processor
client = ConnectClient(api_key=connect_key[0], endpoint=connect_api_url[0])

class TestPurchase(unittest.TestCase):
    # //////////////////////
    # PURCHASE UNIT TESTS
    # /////////////////////

    def test_purchase_pass(self):
        request = TestUtils.get_request("request/create_purchase_request_body.json")
        response = TestUtils.get_request("request/create_purchase_response_body.json")
        if bool(project_manager.purchase):
            project_manager.purchase.Purchase.process_request(request, client)
            self.assertIsInstance(Purchase.process_request(request, client), response)