from connect_processor.app.utils.utils import Utils, get_basic_value
from connect_processor.app.utils.globals import Globals

class Purchase():

    # This method processes the Fulfillment Requests in Pending status for change subscription action

    def process_request(request, client):
        # Type PURCHASE means, it is a new subscription in Connect

        # Create the subscription in vendor system by calling the Vendor API to create subscription

        # The following is the Mock API to create subscription
        # api_client = APIClient(api_url='https://api.conn.rocks/public/v1',
        #                        api_key='ApiKey SU-265-300-494:bec18741a853297bb267b5a4839bd37e72357d89')
        # data = {}
        # subscription_info = api_client.create_subscription(data=data)

        # The response of create subscription Vendor API might have some information that needs to be saved in the fulfillment parameter of subscription in Connect
        vendor_subscription_id = '#'
        # Update the fulfilment parameters in Fulfillment Request in Connect with the corresponding value

        payload = {
            "asset": {
                "params": [
                    {
                        # Customize the fulfillment parameter id, as configured in product in Connect
                        "id": "subscriptionId",
                        "value": vendor_subscription_id,
                        "value_error": "",
                        "structured_value": ""
                    }
                ]
            }
        }

        # This will update the value in the fulfillment parameter
        request_id = get_basic_value(request, 'id')
        fulfillment = client.requests[request_id].update(payload=payload)
        # Approved is the final status of the Fulfillment Request of Subscription in Connect
        # Approve the fulfillment request. The status of fulfillment request will be updated to Approved. And the status of Subscription will get updated to Active.
        payload1 = {"template_id": Globals.ACTIVATION_TEMPLATE}
        # Provide the template id configured as Activation template. This template has the message for the customer that the subscription is successfully provisioned.
        result = client.requests[request_id]('approve').post(payload=payload1)
        # Returning the Activation Template will update the status of Fullfilment Request to Approved and Subscription status to Active.
        # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfillment Request remain empty.











