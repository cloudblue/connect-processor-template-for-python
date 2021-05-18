# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class Change:
    """ Type CHANGE means, it is a change request of an existing active subscription in Connect
        Change request includes request for changing the quantity of subscribed item/SKU or adding/removing items """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """  This method processes the Fulfillment Requests in Pending status for change subscription action.
            If vendor system does not support the change in the subscription check the request details
            to reject the request with proper message. """

        # Get the existing subscription Id saved as fulfilment parameter to Prepare the body/payload for the Vendor API
        # to update the subscription
        # Saving the Subscription ID from Vendor system is encouraged to be able to map the subscription in Connect with
        # the subscription in Vendor system
        # The Subscription ID can be saved in a fulfillment parameter
        # This external_subscription_id from Vendor platform might be required to call the Vendor API to change
        # the subscription
        external_subscription_id = Utils.get_param_value(request, 'fulfillment', 'subscription_id')

        # TODO: Add code to Update/Change the subscription in vendor system by calling the Vendor API
        # to update/change subscription
        # api_client = APIClient(api_url='',
        #                        api_key='')
        # change_payload = {}
        # api_client.change_subscription(change_payload, external_subscription_id)

        # When successful, approve the fulfillment request with the following code:
        return Utils.approve_fulfillment_request(request, client)
        # If change is done, the request is Approved and Subscription status remains Active.
        # If the change can't be done the request can be rejected using Utils.reject_fulfillment_request method.
