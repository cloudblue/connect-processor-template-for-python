# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
import unittest
from cnct import ConnectClient
from connect_processor.app.dynamic_validation import do_validate
from unittest.mock import patch, MagicMock
from tests.test_util import TestUtils

client = ConnectClient('Key', use_specs=False)


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
