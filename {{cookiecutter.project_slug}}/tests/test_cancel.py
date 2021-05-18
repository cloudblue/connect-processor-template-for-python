# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
import unittest
from cnct import ConnectClient
from connect_processor.app.cancel import Cancel
from unittest.mock import patch, MagicMock
from tests.test_util import TestUtils

client = ConnectClient('Key', use_specs=False)


class TestCancel(unittest.TestCase):
    # //////////////////////
    # CANCEL UNIT TESTS
    # /////////////////////

    @patch('connect_processor.app.utils.utils.Utils.approve_fulfillment_request',
           MagicMock(return_value=TestUtils.get_response("purchase_subscription_response.json")))
    @patch('connect_processor.app.utils.utils.Utils._get_template_by_product',
           MagicMock(return_value="TL-###-###-###"))
    def test_cancel_pass(self):
        request = TestUtils.get_response("create_purchase_request_body.json")
        response = TestUtils.get_response("purchase_subscription_response.json")
        result = Cancel.process_request(request, client)
        self.assertDictEqual(result, response)
