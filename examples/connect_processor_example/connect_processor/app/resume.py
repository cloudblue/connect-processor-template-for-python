from .utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class Resume:
    """ Type RESUME means, it is a resume request of an existing suspended subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict,ConnectClient) -> Dict
        """ This method processes the Fulfillment Requests in Pending status for resume subscription action """

        external_subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')

        api_client = Utils.get_api_client()
        resume_payload = {}
        api_client.resume_subscription(resume_payload, external_subscription_id)

        return Utils.approve_fulfillment_request(request, client)
