from connect_ext.utils.utils import Utils

from cnct import ConnectClient

from typing import Dict


class Cancel:
    """ Type CANCEL means, it is a cancel request of an existing subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> None
        """ This method approves or rejects the Fulfillment Requests in Pending status
        for cancel subscription action. """

        external_subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')

        api_client = Utils.get_api_client()
        cancel_payload = {}
        api_client.cancel_subscription(cancel_payload, external_subscription_id)

        Utils.approve_fulfillment_request(request, client)
