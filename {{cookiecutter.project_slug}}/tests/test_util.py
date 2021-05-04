import json
import os


class TestUtils:
    @staticmethod
    def get_request(file, model_class):
        with open(os.path.join(os.path.dirname(__file__), file)) as request_file:
            request = model_class.deserialize(request_file.read())
        return request

    @staticmethod
    def get_response(response, root_folder=None):
        if root_folder:
            return TestUtils.extract_data_file(root_folder + "/request/" + response)
        return TestUtils.extract_data_file("request/" + response)

    @staticmethod
    def extract_data_file(file):
        with open(os.path.join(os.path.dirname(__file__), file)) as config_file:
            data_file = json.load(config_file)
        return data_file

    @staticmethod
    def get_config_file():
        with open('./tests/config.json') as file_handle:
            config = json.load(file_handle)
        return config
