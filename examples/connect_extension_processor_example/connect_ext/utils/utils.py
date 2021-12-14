from typing import Any, Dict

from cnct import ConnectClient

from .message import Message

from connect_ext.app.api_client.isv_client import APIClient

from connect.client.models.resourceset import ResourceSet


class Utils:
    """ Class for all static processor methods. """
    ACTIVATION_TEMPLATE_NAME = 'Default Activation Template'
    API_ENDPOINT = ''

    @staticmethod
    def get_item_by_id(items, item_id):
        # type: (Dict, str) -> object
        """ Finds the item object with the item id name in the structure. """
        for item in items:
            if item['id'] == item_id:
                return item
        raise Exception('Item {id} not found.'.format(id=item_id))

    @staticmethod
    def get_basic_value(base, name):
        # type: (Dict,str) -> Any
        """ Finds in the structure the value for the given name. """
        if base and name in base:
            return base[name]
        return '-'

    @staticmethod
    def get_value(base, prop, value):
        # type: (Dict,str,str) -> Dict
        if prop in base:
            return Utils.get_basic_value(base[prop], value)
        return {}

    @staticmethod
    def update_subscription_parameters(request_id, payload, client):
        # type: (str,object,ConnectClient) -> object
        """ Updates the fulfillment request parameters values in Connect """
        fulfillment_request = client.requests.resource(request_id).update(payload=payload)
        return fulfillment_request

    @staticmethod
    def get_param_value(request, param_phase_value, param_name):
        # type: (Dict, str, str) -> object
        """ Gets the value in the request for the product param name given """
        params = Utils.get_value(request, 'asset', 'params')
        for param in params:
            param_phase = Utils.get_basic_value(param, 'phase')
            if (param_phase == param_phase_value
                    and Utils.get_basic_value(param, 'name') == param_name):
                return Utils.get_basic_value(param, 'value')

    @staticmethod
    def approve_fulfillment_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """ Approves the request with the Client. Its status will be updated to Approved. """
        # Get the subscription product_id
        product = Utils.get_value(request, 'asset', 'product')
        product_id = Utils.get_basic_value(product, 'id')
        # Get the activation template id.
        template_id = Utils._get_template_by_product(product_id, Utils.ACTIVATION_TEMPLATE_NAME,
                                                     'asset', client)
        # Prepare the payload.
        payload = {"template_id": template_id}
        request_id = Utils.get_basic_value(request, 'id')
        # Approve the fulfillment request with the payload
        return Utils._approve_fulfillment_request(request_id, payload, client)

    @staticmethod
    def approve_tier_config_request(request, tcr_id, client):
        # type: (Dict, str, ConnectClient) -> Dict
        """ Approves the tier config request with the Client. Its status will be updated to Approved. """
        # Get the tier config product_id
        product = Utils.get_value(request, 'configuration', 'product')
        product_id = Utils.get_basic_value(product, 'id')
        template_id = Utils._get_template_by_product(product_id, Utils.ACTIVATION_TEMPLATE_NAME,
                                                     'tier1', client)
        payload = {
            "template": {
                "id": template_id
            }
        }
        return Utils._approve_tier_config_request(tcr_id, payload, client)

    @staticmethod
    def _approve_fulfillment_request(request_id, payload, client):
        # type: (str,object,ConnectClient) -> Dict
        result = client.requests[request_id].action(name="approve")
        approve_result = result.post(payload=payload)
        return approve_result

    @staticmethod
    def reject_fulfillment_request(request_id, reason, client):
        # type: (str,str,ConnectClient) -> object
        """ Rejects the fulfillment request. Its status will be updated to Failed. """
        # Prepare the reject payload.
        payload = {
            "reason": reason
        }
        result = client.requests[request_id].action(name="fail")
        reject_result = result.post(payload=payload)
        return reject_result

    @staticmethod
    def _get_template_by_product(product_id, template_name, template_scope, client):
        # type: (str,str, str, ConnectClient) -> str
        """ Finds the the template for the product and scope. """
        template = client.collection('products')[product_id].templates.filter(name=template_name,
                                                                              scope=template_scope).first()
        template_id = Utils.get_basic_value(template, 'id')
        return template_id

    @staticmethod
    def update_tier1_parameters(tcr_id, payload, client):
        # type: (str, object, ConnectClient) -> object
        """ Updates the tier1 parameters in the fulfillment request. """
        tier_request = client.ns('tier').collection('config-requests')[tcr_id].update(payload=payload)
        return tier_request

    @staticmethod
    def _approve_tier_config_request(tcr_id, payload, client):
        # type: (str,object, ConnectClient) -> Dict
        """ Approves the Tier Config request. Its status will be updated to Approved.
            The status of Tier Config will get updated to Active.
            The status of Subscription will get updated to Pending. """
        result = client.ns('tier').collection('config-requests')[tcr_id].action(name="approve")
        approve_result = result.post(payload=payload)
        return approve_result

    @staticmethod
    def get_api_client():
        return APIClient(Utils.API_ENDPOINT)

    @staticmethod
    def save_error(client, request_id, error_message):
        # type: (ConnectClient,str, str) -> Any
        """ Stores the error message in the Fulfillment Request conversation """
        conversations = ResourceSet(client, path='conversations', query='instance_id=' + request_id)
        if conversations.count() > 0:
            conversation_id = conversations[0]['id']
            value = error_message

            data = {
                "text": Message.PROCESSING_REQUEST_ERROR.format(value),
                "type": "message"
            }
            result = client.conversations[conversation_id].action(name="messages")
            result.post(payload=data)
