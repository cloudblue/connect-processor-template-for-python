import json
from typing import Any, Dict

class Utils:

    @staticmethod
    def get_config_file() -> Dict[str, Any]:
        with open("./config.json") as file_handle:
            config = json.load(file_handle)
        return config


    @staticmethod
    def is_null_or_empty(value):
        return value is None or value == 0 or len(value) == 0


    @staticmethod
    def get_item_by_id(items, item_id) -> object:
        for item in items:
            if item['id'] == item_id:
                return item
        raise Exception('Item {id} not found.'.format(id=item_id))


def get_basic_value(base, value):
    if base and value in base:
        return base[value]
    return '-'

def get_value(base, prop, value):
    if prop in base:
        return get_basic_value(base[prop], value)
    return '-'


