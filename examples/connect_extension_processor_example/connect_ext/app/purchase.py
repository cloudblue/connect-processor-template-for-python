from connect_ext.utils.utils import Utils

from cnct import ConnectClient

from typing import Dict


class Purchase:
    """ Type PURCHASE means, it is a new subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> None
        """ This method processes the Fulfillment Requests in Pending status for purchase subscription action """

        api_client = Utils.get_api_client()
        subscription_info = api_client.create_subscription({})
        # In this Product Example is assumed the subscription is created always with one Connect item,
        # without noticing the item MPN or SKU.
        Purchase._create_licenses(request, api_client, subscription_info['tenantId'])

        Purchase._save_fulfillment_parameters(request, client, subscription_info)

        Utils.approve_fulfillment_request(request, client)

    @staticmethod
    def _save_fulfillment_parameters(request, client, subscription_info):
        # type: (Dict, ConnectClient, Dict) -> None
        subscription_id = subscription_info['tenantId']
        request_id = Utils.get_basic_value(request, 'id')

        payload = {
            "asset": {
                "params": [
                    {
                        "id": "subscription_id",
                        "value": subscription_id,
                        "value_error": "",
                        "structured_value": {}
                    }
                ]
            }
        }
        Utils.update_subscription_parameters(request_id, payload, client)

    @staticmethod
    def _create_licenses(request, api_client, subscription_id):
        quantity = Utils.get_value(request, 'asset', 'items')[0]['quantity']
        payload = {
            "licences": {
                "limit": quantity
            }
        }
        api_client.change_subscription(payload, subscription_id)
