from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class Suspend:
    """ Type SUSPEND means, it is a suspend request of an existing active subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """ This method processes the Fulfillment Requests in Pending status for suspend subscription action """

        # Get the subscription Id from the request that needs to be suspended
        # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect
        # with the subscription in Vendor system
        # The Subscription ID can be saved in a fulfillment parameter
        # This external_subscription_id from Vendor platform might be required to call the Vendor API
        # to suspend subscription
        external_subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')

        # TODO: Add code to Suspend the subscription in vendor system by calling the Vendor API
        # to resume subscription
        # api_client = APIClient(api_url='',
        #                        api_key='')
        # suspend_payload = {}
        # api_client.suspend_subscription(suspend_payload, external_subscription_id)

        # When successful, approve the fulfillment request with the following code:
        return Utils.approve_fulfillment_request(request, client)
        # If suspend action is ok the Fulfillment Request object status will be Approved and
        # the Subscription object Suspended.
        # If the suspend action can't be done the request can be rejected using Utils.reject_fulfillment_request method.
