from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class Cancel:
    """ Type CANCEL means, it is a cancel request of an existing subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """ This method approves or rejects the Fulfillment Requests in Pending status
        for cancel subscription action. """

        # Get the fulfillment parameter values from the subscription that needs to be cancelled
        # Saving the Subscription ID from Vendor system is encouraged to be able to map the Connect subscription
        # with the subscription in Vendor system. The Subscription ID can be saved in a fulfillment parameter.
        # Here 'subscription_id' is an example of Connect product fulfillment parameter id.
        # This external_subscription_id from Vendor platform might be required to call the Vendor API
        # to cancel the subscription
        external_subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')

        # TODO: Add your code to Cancel the subscription in vendor system by calling the Vendor API
        # api_client = APIClient(api_url='',
        #                        api_key='')
        # cancel_payload = {}
        # api_client.cancel_subscription(cancel_payload, external_subscription_id)

        # When successful, approve the fulfillment request with the following code:
        return Utils.approve_fulfillment_request(request, client)
        # If cancellation is done, the request is Approved and Subscription object status to Terminated.
        # If cancellation can't be done is can be rejected using Utils.reject_fulfillment_request method.
