# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class TierConfiguration:
    """ Type TIER CONFIGURATION means, the request has required data for subscription provisioning from
    the Reseller/Tier1. This request type can be 'setup' (only the first time the reseller places a purchase request),
    or 'update' (each time the reseller needs to change any tier scope parameter value)) """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """ This method processes a tier configuration request in pending status for setup and update action. """

        # Check the reseller data in vendor system by calling the Vendor API
        # TODO: implement the Vendor API call to check, create or update the reseller in Vendor portal
        # The following is the Mock API and client to check tier scope ordering phase parameters
        # api_client = APIClient(api_url='',
        #                        api_key='')
        # data = {}
        # reseller_info = api_client.check_reseller(data=data)
        tcr_id = Utils.get_basic_value(request, 'id')

        # The response of check reseller Vendor API might have some information that needs to be saved in
        # the fulfillment parameter of the tier config request in Connect
        # With this response complete the tier config fulfillment parameters to be able to approve the request
        TierConfiguration._save_fulfillment_parameters(request, client)

        # If any tier scope parameter is not valid, the tier config request can be changed to Inquiring status,
        # so the reseller can change and check the entered values
        # using this method call Utils.set_inquiring_tier_config_request(tcr_id, client)

        return Utils.approve_tier_config_request(request, tcr_id, client)
        # The status of Tier Configuration is Active and linked Subscription status changes to Pending.
        # Approved is the final status of a Tier Config Request in Connect
        # If any of the mandatory/required fulfilment parameters are not valid for the request,
        # it can be set their value_error property and the Tier Config request will change to Inquiring status.

    @staticmethod
    def _save_fulfillment_parameters(request, client):
        # type: (Dict, ConnectClient) -> None
        """ This method saves the needed information of the reseller in the tier config request's fulfillment
            parameters. Customize the Payload params ids with your product tier fulfillment parameters id in Connect and
            the params values with the ones given by the Vendor API. """

        tcr_id = Utils.get_basic_value(request, 'id')

        # Prepare the update parameters payload with the response of APIClient.create_subscription method
        payload = {
            "params": [
                {
                    # TODO: Customize the tier fulfillment parameter id, as configured in product in Connect
                    "id": "param_a",
                    "value": "value for param_a in Vendor System",
                    "value_error": "",
                    "structured_value": ""
                },
                {
                    # TODO: Change and/or add the tier fulfillment parameters id, as configured in product in Connect
                    "id": "param_b",
                    "value": "value for param b in Vendor System",
                    "value_error": "",
                    "structured_value": ""
                }
            ]
        }

        # Update the value in the fulfillment parameter of the tier configuration
        Utils.update_tier1_parameters(tcr_id, payload, client)
