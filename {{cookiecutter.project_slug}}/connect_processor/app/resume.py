from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class Resume:
    """ Type RESUME means, it is a resume request of an existing suspended subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """ This method processes the Fulfillment Requests in Pending status for resume subscription action """

        # Get the subscription Id from the request that needs to be resumed
        # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect
        # with the subscription in Vendor system
        # The Subscription ID can be saved in a fulfillment parameter
        # This external_subscription_id from Vendor platform might be required to call the Vendor API
        # to resume the suspended subscription
        external_subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')

        # TODO: Add code to Resume the subscription in vendor system by calling the Vendor API
        # to resume subscription
        # api_client = APIClient(api_url='',
        #                        api_key='')
        # resume_payload = {}
        # api_client.resume_subscription(resume_payload, external_subscription_id)

        # When successful, approve the fulfillment request with the following code:
        return Utils.approve_fulfillment_request(request, client)
        # If resume is ok the status of Fulfillment Request object will be Approved and Subscription object Active.
        # If the resume action can't be done the request can be rejected using Utils.reject_fulfillment_request method.
