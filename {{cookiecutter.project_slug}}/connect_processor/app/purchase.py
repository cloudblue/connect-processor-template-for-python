from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class Purchase:
    """ Type PURCHASE means, it is a new subscription in Connect """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """ This method processes the Fulfillment Requests in Pending status for purchase subscription action """

        # Create the subscription in vendor system by calling the Vendor API to create subscription
        # TODO: implement the Vendor API call to create the subscription in Vendor portal
        # The following is the Mock API and client to create subscription
        # api_client = APIClient(api_url='',
        #                        api_key='')
        # data = {}
        # subscription_info = api_client.create_subscription(data=data)

        # The response of create subscription Vendor API might have some information that needs to be saved in
        # the fulfillment parameter of the subscription request in Connect
        # With this response complete the request fulfillment parameters to be able to approve the request
        Purchase._save_fulfillment_parameters(request, client)

        return Utils.approve_fulfillment_request(request, client)
        # The status of Fulfillment Request is Approved and Subscription is Active.
        # Approved is the final status of the Fulfillment Request of Subscription in Connect
        # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter
        # in Fulfillment Request remain empty.

    @staticmethod
    def _save_fulfillment_parameters(request, client):
        # type: (Dict, ConnectClient) -> None
        """ This method saves the needed information of the created subscription in the request's fulfillment
            parameters. Customize the Payload params ids with your product fulfillment parameters id in Connect and
            the params values with the ones given by the Vendor API. """

        request_id = Utils.get_basic_value(request, 'id')
        # Update the fulfilment parameters in Fulfillment Request in Connect with the corresponding value

        # Prepare the update parameters payload with the response of APIClient.create_subscription method
        payload = {
            "asset": {
                "params": [
                    {
                        # TODO: Customize the fulfillment parameter id, as configured in product in Connect
                        # Saving the Subscription ID from Vendor system is encouraged to be able to map
                        # the subscription in Connect with the subscription in Vendor system
                        "id": "subscription_id",
                        "value": "value for subscription ID in Vendor System",
                        "value_error": "",
                        "structured_value": ""
                    },
                    {
                        # TODO: Change and/or add the fulfillment parameters id, as configured in product in Connect
                        "id": "param_b",
                        "value": "value for parameter b",
                        "value_error": "",
                        "structured_value": ""
                    }
                ]
            }
        }

        # Update the value in the fulfillment parameter
        Utils.update_subscription_parameters(request_id, payload, client)
