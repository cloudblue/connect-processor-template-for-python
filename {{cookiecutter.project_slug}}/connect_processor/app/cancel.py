from connect_processor.app.utils.utils import Utils, get_basic_value
from connect_processor.app.utils.globals import Globals

class Cancel():

    # This method processes the Fulfillment Requests in Pending status for cancel/terminate subscription action

    def process_request(request, client):
        # Type CANCEL means, it is a cancel request of an existing subscription in Connect

        # Get the subscription Id from the request that needs to be cancelled
        params = get_basic_value('asset', 'params')
        for param in params:
            param_type = get_basic_value(param, 'phase')
            # The 'param_a' is the id of fulfillment parameter
            # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect with the subscription in Vendor system
            # The Subscription ID can be saved in a fulfillment parameter
            if param_type == 'fulfillment' and get_basic_value(param, 'name') == 'param_a':
                external_subscription_id = get_basic_value(param, 'value')
                # This external_subscription_id from Vendor platform might be required to call the Vendor API to cancel subscription

        # Customize: Add code to Cancel the subscription in vendor system by calling the Vendor API to cancel/terminate subscription
        # When successful, approve the fulfillment request

        # Provide the template id configured as Activation template. This template has the message for the customer that the subscription is terminated.
        # Get the template
        product = get_value(request, 'asset', 'product')
        product_id = get_basic_value(product, 'id')
        template = client.collection('products')[product_id].templates.filter(name=('Default Activation Template'),
                                                                              scope=('asset')).first()
        # Customize: Change the template name to match with the name configured in Product in Connect
        template_id = get_basic_value(template, 'id')
        payload1 = {"template_id": template_id}
        request_id = get_basic_value(request, 'id')
        result = Cancel.approve_request(request_id, payload, client)
        return result
        # Returning the Activation Template will update the status of Fullfilment Request object to Approved and Subscription object status to Terminated.
        # The statuses will not get updated as Approved and Terminated if any of the mandatory/required fulfilment parameter in Fullfilment Request remain empty.

    def approve_request(request_id, payload, client):
        # Approve the fulfillment request. The status of Fulfillment Request object to Approved and Subscription object status to Terminated.
        result = client.requests[request_id].approve
        change_result = result.post(payload=payload)
        return change_result




