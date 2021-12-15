from connect_ext.utils.utils import Utils

from cnct import ConnectClient

from typing import Dict


class Suspend:
    """ Type SUSPEND means, it is a suspend request of an existing active subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict,ConnectClient) -> Dict
        """ This method processes the Fulfillment Requests in Pending status for suspend subscription action """

        external_subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')

        api_client = Utils.get_api_client()
        suspend_payload = {}
        api_client.suspend_subscription(suspend_payload, external_subscription_id)

        Utils.approve_fulfillment_request(request, client)
