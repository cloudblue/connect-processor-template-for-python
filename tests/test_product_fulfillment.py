from tests.test_utils import TestUtils
import unittest
from unittest.mock import patch, MagicMock
from app.product_fulfillment import ProductFulfillment
# from app.tier_fulfillment import TierConfiguration
from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.models import ActivationTemplateResponse, TierConfigRequest, TierConfig, Fulfillment


@patch('requests.put', MagicMock(status_code=200))

@patch('app.utils.utils.Utils.get_config_file', MagicMock(return_value=TestUtils.get_config_file()))
@patch("app.product_fulfillment.ProductFulfillment.update_parameters", MagicMock(return_value=''))
class TestProductFulfillment(unittest.TestCase):

    # //////////////////////
    # PURCHASE UNIT TESTS
    # /////////////////////

    # Use the below to mock the API response
    # @patch('app.product_fulfillment.ProductFulfillment._create_subscription',
    #        MagicMock(return_value=TestUtils.get_response("create_purchase_request_response")))

    def test_purchase_pass(self):
        request = TestUtils.get_request("request/create_purchase_request_body.json", Fulfillment)
        product_fulfillment = TestUtils.get_product_fulfillment(ProductFulfillment)
        print(ActivationTemplateResponse)
        self.assertIsInstance(product_fulfillment.process_request(request), ActivationTemplateResponse)

    # Use the below test to test the purchase fail case
    # def test_purchase_fail(self):
    #     request = TestUtils.get_request("//Cloud PdM - ESP/Dev Program for Vendors/Example Processor/tests/request/create_purchase_request_fail_body.json",
    #                                     Fulfillment)
    #     product_fulfillment = TestUtils.get_product_fulfillment(ProductFulfillment)
    #     with self.assertRaises(SkipRequest):
    #         product_fulfillment.process_request(request)

    # //////////////////////
    # CHANGE UNIT TESTS
    # /////////////////////



    def test_change_pass(self):
        request = TestUtils.get_request("request/change_request_body.json", Fulfillment)
        product_fulfillment = TestUtils.get_product_fulfillment(ProductFulfillment)
        # resp = TestUtils.get_response("change_request_body")
        # self.assertEqual(resp["statusCode"], "ACTIVE")
        self.assertIsInstance(product_fulfillment.process_request(request), ActivationTemplateResponse)

    # //////////////////////
    # CANCEL UNIT TESTS
    # //////////////////////


    def test_cancel_pass(self):
        request = TestUtils.get_request(
            "request/cancel_request_body.json",
            Fulfillment)
        product_fulfillment = TestUtils.get_product_fulfillment(ProductFulfillment)
        self.assertIsInstance(product_fulfillment.process_request(request), ActivationTemplateResponse)

    # //////////////////////
    # SUSPEND UNIT TESTS
    # //////////////////////


    def test_suspend_pass(self):
        request = TestUtils.get_request(
            "request/suspend_request_body.json",
            Fulfillment)
        product_fulfillment = TestUtils.get_product_fulfillment(ProductFulfillment)
        self.assertIsInstance(product_fulfillment.process_request(request), ActivationTemplateResponse)


    # //////////////////////
    # RESUME UNIT TESTS
    # //////////////////////


    def test_resume_pass(self):
        request = TestUtils.get_request(
            "request/resume_request_body.json",
            Fulfillment)
        product_fulfillment = TestUtils.get_product_fulfillment(ProductFulfillment)
        self.assertIsInstance(product_fulfillment.process_request(request), ActivationTemplateResponse)
