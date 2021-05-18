# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
import unittest
from cnct import ConnectClient
from unittest.mock import patch, MagicMock
from tests.test_util import TestUtils
from connect_processor.app.suspend import Suspend

client = ConnectClient('Key', use_specs=False)


class TestSuspend(unittest.TestCase):
    # //////////////////////
    # SUSPEND UNIT TESTS
    # /////////////////////

    @patch('connect_processor.app.utils.utils.Utils.approve_fulfillment_request',
           MagicMock(return_value=TestUtils.get_response("purchase_subscription_response.json")))
    @patch('connect_processor.app.utils.utils.Utils._get_template_by_product',
           MagicMock(return_value="TL-###-###-###"))
    def test_suspend_pass(self):
        request = TestUtils.get_response("create_purchase_request_body.json")
        response = TestUtils.get_response("purchase_subscription_response.json")
        result = Suspend.process_request(request, client)
        self.assertDictEqual(result, response)
