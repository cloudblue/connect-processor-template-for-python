# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
import json
import os

from typing import Any, Dict


class TestUtils:

    @staticmethod
    def get_response(response, root_folder=None):
        # type: (str, str) -> Any
        """ Loads the response file name from the request folder for test purposes. """
        if root_folder:
            return TestUtils._extract_data_file(root_folder + "/request/" + response)
        return TestUtils._extract_data_file("request/" + response)

    @staticmethod
    def _extract_data_file(file):
        with open(os.path.join(os.path.dirname(__file__), file)) as config_file:
            data_file = json.load(config_file)
        return data_file

    @staticmethod
    def get_config_file():
        # type: () -> Dict[str, Any]
        """ Loads the config file for test purposes. """
        with open('./tests/config.json') as file_handle:
            config = json.load(file_handle)
        return config
