from connect_processor.app.utils.utils import Utils
from connect_processor.app.utils.globals import Globals

class Suspend():

    # This method processes the Fulfillment Requests in Pending status for suspend subscription action

    def process_request(request, client):
        # Type SUSPEND means, it is a suspend request of an existing active subscription in Connect

        # Get the subscription Id from the request that needs to be suspended
        params = Utils.get_basic_value('asset', 'params')
        for param in params:
            param_type = Utils.get_basic_value(param, 'phase')
            # The 'param_a' is the id of fulfillment parameter
            # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect with the subscription in Vendor system
            # The Subscription ID can be saved in a fulfillment parameter
            if param_type == 'fulfillment' and Utils.get_basic_value(param, 'name') == 'param_a':
                external_subscription_id = Utils.get_basic_value(param, 'value')
                # This external_subscription_id from Vendor platform might be required to call the Vendor API to suspend subscription

        # Customize: Add code to Suspend the subscription in vendor system by calling the Vendor API to suspend subscription
        # When successful, approve the fulfillment request

        # Provide the template id configured as Activation template. This template has the message for the customer that the subscription is suspended.
        # Get the template
        product = Utils.get_value(request, 'asset', 'product')
        product_id = Utils.get_basic_value(product, 'id')

        # Customize: Change the template name to match with the name configured in Product in Connect
        template_id = Utils.get_template_by_product(product_id, 'Default Activation Template', 'asset', client)
        payload = {"template_id": template_id}
        request_id = Utils.get_basic_value(request, 'id')
        # Approve the fulfillment request with the template
        result = Utils.approve_fulfillment_request(request_id, payload, client)
        return result
        # Returning the Activation Template will update the status of Fulfillment Request object to Approved and Subscription object status to Suspended.
        # The statuses will not get updated as Approved and Suspended if any of the mandatory/required fulfilment parameter in Fulfillment Request remain empty.
        # Another template can be created in Vendor Portal. Pass the Template Id to use it.





