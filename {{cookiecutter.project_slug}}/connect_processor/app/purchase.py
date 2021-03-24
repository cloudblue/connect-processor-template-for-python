from connect_processor.app.utils.utils import Utils, get_basic_value, get_value
from connect_processor.app.utils.globals import Globals

class Purchase():

    # This method processes the Fulfillment Requests in Pending status for change subscription action

    def process_request(request, client):
        # Type PURCHASE means, it is a new subscription in Connect

        request_id = get_basic_value(request, 'id')

        # Create the subscription in vendor system by calling the Vendor API to create subscription
        # Customize: implement the Vendor API call to create the subscription in Vendor portal

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

        # This will update the value in the fulfillment parameter
        fulfillment_request = Purchase.update_parameters(request_id, payload, client)

        # Approved is the final status of the Fulfillment Request of Subscription in Connect
        # Provide the template id configured as Activation template. This template has the message for the customer that the subscription is successfully provisioned.

        # Get the template
        product = get_value(request, 'asset', 'product')
        product_id = get_basic_value(product, 'id')
        template = client.collection('products')[product_id].templates.filter(name=('Default Activation Template'), scope=('asset')).first()
        # Customize: Change the template name to match with the name configured in Product in Connect
        template_id = get_basic_value(template, 'id')
        payload1 = {"template_id": template_id}

        # Approve the fulfillment request with the template
        purchase_result = Purchase.approve_request(request_id, payload1, client)
        return purchase_result
        # This will update the status of Fullfilment Request to Approved and Subscription status to Active.
        # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfillment Request remain empty.

    def update_parameters(request_id, payload, client):
        # This will update the value in the parameters in the fulfillment request
        fulfillment_request = client.requests.resource(request_id).update(payload=payload)
        return fulfillment_request

    def approve_request(request_id, payload, client):
        # Approve the fulfillment request. The status of fulfillment request will be updated to Approved. And the status of Subscription will get updated to Active.
        result = client.requests[request_id].approve
        purchase_result = result.post(payload=payload)
        return purchase_result