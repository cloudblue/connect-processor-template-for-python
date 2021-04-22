import json
from typing import Any, Dict

class Utils:

    @staticmethod
    def get_config_file() -> Dict[str, Any]:
        with open("./config.json") as file_handle:
            config = json.load(file_handle)
        return config


    @staticmethod
    def get_item_by_id(items, item_id) -> object:
        for item in items:
            if item['id'] == item_id:
                return item
        raise Exception('Item {id} not found.'.format(id=item_id))

    @staticmethod
    def get_basic_value(base, value):
        if base and value in base:
            return base[value]
        return '-'

    @staticmethod
    def get_value(base, prop, value):
        if prop in base:
            return Utils.get_basic_value(base[prop], value)
        return '-'

    @staticmethod
    def update_subscription_parameters(request_id, payload, client):
        # This will update the value in the parameters in the fulfillment request
        fulfillment_request = client.requests.resource(request_id).update(payload=payload)
        return fulfillment_request

    @staticmethod
    def approve_fulfillment_request(request_id, payload, client):
        # Approve the fulfillment request. The status of fulfillment request will be updated to Approved.
        result = client.requests.resource(request_id).approve
        purchase_result = result.post(payload=payload)
        return purchase_result

    @staticmethod
    def get_template_by_product(product_id, template_name, template_scope, client):
        template = client.collection('products')[product_id].templates.filter(name=(template_name),
                                                                              scope=(template_scope)).first()
        template_id = Utils.get_basic_value(template, 'id')
        return template_id

    def update_Tier1_parameters(tcr_id, payload, client):
        # This will update the value in the parameters in the fulfillment request
        tier_request = client.ns('tier').collection('config-requests')[tcr_id].update(payload=payload)
        return tier_request

    def approve_Tier_config_request(tcr_id, payload, client):
        # Approve the fulfillment request. The status of tier config request will be updated to Approved.
        # The status of Tier Config will get updated to Active.
        # The status of Subscription will get updated to Pending.
        result = client.ns('tier').collection('config-requests')[tcr_id].approve
        purchase_result = result.post(payload=payload)
        return purchase_result








