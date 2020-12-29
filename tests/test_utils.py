import json
import os
from connect.config import Config
from typing import Dict, Any

class TestUtils:

    @staticmethod
    def get_request(file, model_class):
        with open(os.path.join(os.path.dirname(__file__), file)) as request_file:
            request = model_class.deserialize(request_file.read())
        return request
    # @staticmethod
    # def get_request(response, root_folder=None):
    #     if root_folder:
    #         return TestUtils.extract_data_file(root_folder + "/request/" + response + ".json")
    #     return TestUtils.extract_data_file("request/" + response + ".json")

    @staticmethod
    def get_response(response, root_folder=None):
        if root_folder:
            return TestUtils.extract_data_file(root_folder+"/response/" + response + ".json")
        return TestUtils.extract_data_file("response/" + response + ".json")

    @staticmethod
    def extract_data_file(file):
        with open(os.path.join(os.path.dirname(__file__), file)) as config_file:
            data_file = json.load(config_file)
        return data_file

    @staticmethod
    def get_product_fulfillment(fulfillment):
        config_file = TestUtils.get_config_file()
        fulfillment_automation = fulfillment(Config(
            api_url=config_file['apiEndpoint'],
            api_key=config_file['apiKey'],
            products=config_file['products']
        ))
        return fulfillment_automation

    @staticmethod
    def get_tier_configuration(tierconfig):
        config_file = TestUtils.get_config_file()
        tier_automation = tierconfig(Config(
            api_url=config_file['apiEndpoint'],
            api_key=config_file['apiKey'],
            products=config_file['products']
        ))
        return tier_automation

    @staticmethod
    def get_config_file() -> Dict[str, Any]:
        with open('./config.json') as file_handle:
            config = json.load(file_handle)
        return config