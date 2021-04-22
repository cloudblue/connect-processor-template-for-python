
from connect_processor.app.utils.utils import Utils
from connect_processor.app.utils.globals import Globals



class Change():

    # This method processes the Fulfillment Requests in Pending status for change subscription action

    def process_request(request, client):
        # The req, parameter of process_request, is an object for Fulfilment Request for the Subscription in Connect

        # Type CHANGE means, it is a change request of an existing active subscription in Connect
        # Change request includes request for changing the quantity of subscribed item/SKU
        # or adding more items

        # If the business does not support downsize, check if any item quantity is reduced.
        # If yes, fail the request with proper message.

        # Get the existing subscription Id saved as fulfilment parameter to Prepare the body/payload for the Vendor API to update the subscription
        params = Utils.get_basic_value('asset', 'params')
        for param in params:
            param_type = Utils.get_basic_value(param, 'phase')
            # The 'param_a' is the id of fulfillment parameter
            # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect with the subscription in Vendor system
            # The Subscription ID can be saved in a fulfillment parameter
            if param_type == 'fulfillment' and Utils.get_basic_value(param, 'name') == 'param_a':
                external_subscription_id = Utils.get_basic_value(param, 'value')
                # This external_subscription_id from Vendor platform might be required to call the Vendor API to cancel subscription

        # Customize: Add code to Update/Change the subscription in vendor system by calling the Vendor API to update/change subscription

        # Get the template
        product = Utils.get_value(request, 'asset', 'product')
        product_id = Utils.get_basic_value(product, 'id')
        template_id = Utils.get_template_by_product(product_id, 'Default Activation Template', 'asset', client)
        payload = {"template_id": template_id}
        request_id = Utils.get_basic_value(request, 'id')
        # Approve the fulfillment request with the template
        result = Utils.approve_fulfillment_request(request_id, payload, client)
        # Update the status of Fulfillment Request to Approved and Subscription status remains Active.
        return result
        # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfillment Request remain empty.


