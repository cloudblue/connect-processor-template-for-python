
from connect_processor.app.utils.utils import Utils, get_basic_value, get_value
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
        params = get_basic_value('asset', 'params')
        for param in params:
            param_type = get_basic_value(param, 'phase')
            # The 'param_a' is the id of fulfillment parameter
            # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect with the subscription in Vendor system
            # The Subscription ID can be saved in a fulfillment parameter
            if param_type == 'fulfillment' and get_basic_value(param, 'name') == 'param_a':
                external_subscription_id = get_basic_value(param, 'value')
                # This external_subscription_id from Vendor platform might be required to call the Vendor API to cancel subscription

        # Customize: Add code to Update/Change the subscription in vendor system by calling the Vendor API to update/change subscription

        payload = {"template_id": Globals.SUBSCRIPTION_APPROVED_TEMPLATE}
        request_id = get_basic_value(request, 'id')
        result = client.requests.resource(request_id)('approve').post(payload=payload)
        # Approve the fulfillment request. The status of Fulfillment Request object to Approved and Subscription object status remains Active.
        # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfillment Request remain empty.


