# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from typing import Dict


class TierConfiguration:

    """ The purpose of the Tier Config is to get the data required for provisioning from the Reseller/Tier1
        The Reseller receives an Activation form with information """

    @staticmethod
    def process_request(request, client):
        # type: (Dict, ConnectClient) -> Dict
        """ Processes the request for the tier config. """

        tcr_id = Utils.get_basic_value(request, 'id')

        # Updating the status of TCR from Inquiring to Pending
        # This step is not required in Production environment.
        # because this status gets updated from Inquiring to Pending when the Reseller/Tier1 submits
        # the required information in the Activation form made available to him in the Commerce platform
        # TODO: Remove this step. It is added for the ease of debug and unit tests
        tcr_status = Utils.get_basic_value(request, 'status')

        if tcr_status == 'inquiring':
            tcr_pending = client.ns('tier').collection('config_requests')[tcr_id]('pend').post(payload={})

        # Updating mandatory/required information in the parameters of scope tier.
        # This step is not required in Production environment.
        # Because this information will get updated when the Reseller fills in the information
        # in the Activation form made available to them in a link in  Commerce Platform
        # TODO: Remove this step
        info_for_tier = "Information from the reseller"
        payload = {
            "params": [{
                "id": "Info_for_tier",
                "value": info_for_tier,
                "value_error": "",
                "structured_value": ""}]}

        update_tier_parameter = Utils.update_tier1_parameters(tcr_id, payload, client)

        # Update the status to Approved
        # The status will not get updated to Approved if any required/mandatory tier parameter is empty
        return Utils.approve_tier_config_request(request, tcr_id, client)
        # The status of Tier Config is Approved and Subscription is Inquiring.
        # Approved is the final status of a Tier Config Request in Connect
        # If any of the mandatory/required fulfilment parameters are not valid for the request,
        # it can be set their value_error property and the Tier Config request will change to Inquiring status.
