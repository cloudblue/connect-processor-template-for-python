from connect_processor.app.utils.utils import Utils
from connect_processor.app.utils.globals import Globals
class Purchase():

    # This method processes the Fulfillment Requests in Pending status for change subscription action

    def process_request(request, client):
        # Type PURCHASE means, it is a new subscription in Connect

        request_id = Utils.get_basic_value(request, 'id')

        # Create the subscription in vendor system by calling the Vendor API to create subscription
        # Customize: implement the Vendor API call to create the subscription in Vendor portal

        # The following is the Mock API and client to create subscription
        # api_client = APIClient(api_url='',
        #                        api_key='')
        # data = {}
        # subscription_info = api_client.create_subscription(data=data)

        # The response of create subscription Vendor API might have some information that needs to be saved in the fulfillment parameter of subscription in Connect
        vendor_subscription_id = '#'
        # Update the fulfilment parameters in Fulfillment Request in Connect with the corresponding value

        payload = {
            "asset": {
                "params": [
                    {
                        # Customize: the fulfillment parameter id, as configured in product in Connect
                        # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect with the subscription in Vendor system
                        "id": "param_a",
                        "value": "value for parameter a",
                        "value_error": "",
                        "structured_value": ""
                    },
                    {
                        # Customize: the fulfillment parameter id, as configured in product in Connect
                        "id": "param_b",
                        "value": "value for parameter b",
                        "value_error": "",
                        "structured_value": ""
                    }
                ]
            }
        }

        # Update the value in the fulfillment parameter
        fulfillment_request = Utils.update_subscription_parameters(request_id, payload, client)

        # Approved is the final status of the Fulfillment Request of Subscription in Connect
        # Provide the template id configured as Activation template. This template has the message for the customer that the subscription is successfully provisioned.

        # Get the template
        product = Utils.get_value(request, 'asset', 'product')
        product_id = Utils.get_basic_value(product, 'id')
        template_id = Utils.get_template_by_product(product_id, 'Default Activation Template', 'asset', client)
        # Customize: Change the template name to match with the name configured in Product in Connect

        payload1 = {"template_id": template_id}

        # Approve the fulfillment request with the template
        purchase_result = Utils.approve_fulfillment_request(request_id, payload1, client)
        return purchase_result
        # Update the status of Fulfillment Request to Approved and Subscription status gets updated to Active.
        # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfillment Request remain empty.

