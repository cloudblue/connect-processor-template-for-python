# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
import unittest
from cnct import ConnectClient
from connect_processor.app.tier_fulfillment import TierConfiguration
from unittest.mock import patch, MagicMock
from tests.test_util import TestUtils

client = ConnectClient('Key', use_specs=False)


class TestTierConfiguration(unittest.TestCase):
    # //////////////////////
    # TIER CONFIGURATION UNIT TESTS
    # /////////////////////

    @patch('connect_processor.app.utils.utils.Utils.update_tier1_parameters',
           MagicMock(return_value=""))
    @patch('connect_processor.app.utils.utils.Utils._approve_tier_config_request',
           MagicMock(return_value=TestUtils.get_response("purchase_subscription_response.json")))
    @patch('connect_processor.app.utils.utils.Utils._get_template_by_product',
           MagicMock(return_value="TL-###-###-###"))
    def test_purchase_pass(self):
        request = TestUtils.get_response("create_purchase_request_body.json")
        response = TestUtils.get_response("purchase_subscription_response.json")
        result = TierConfiguration.process_request(request, client)
        self.assertDictEqual(result, response)
