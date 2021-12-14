from connect_ext.utils.utils import Utils

from cnct import ConnectClient

from typing import Dict


class Change:
    """ Type CHANGE means, it is a change request of an existing active subscription in Connect
        Change request includes request for changing the quantity of subscribed item/SKU or adding/removing items """

    @staticmethod
    def process_request(request, client):
        # type: (Dict,ConnectClient) -> None
        """  This method processes the Fulfillment Requests in Pending status for change subscription action.
            If vendor system does not support the change in the subscription check the request details
            to reject the request with proper message. """

        subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')
        # In this Product Example up/downsizes are allowed, Upgrades or downgrades does not.
        if len(Utils.get_value(request, 'asset', 'items')) == 1:
            new_quantity = Utils.get_value(request, 'asset', 'items')[0]['quantity']

            api_client = Utils.get_api_client()
            change_payload = {
                "licences": {
                    "limit": new_quantity
                }
            }
            api_client.change_subscription(change_payload, subscription_id)

            Utils.approve_fulfillment_request(request, client)
        else:
            request_id = Utils.get_basic_value(request, 'id')
            reason = 'Change not allowed'
            Utils.reject_fulfillment_request(request_id, reason, client)
