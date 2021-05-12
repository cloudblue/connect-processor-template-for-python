# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
from cnct import ConnectClient
from datetime import datetime
from connect_processor.app.utils.globals import Globals
from connect_processor.app.utils.utils import Utils
from cnct import R

project_manager = __import__('connect_processor.app', globals(), locals(),
                             ['purchase', 'change', 'cancel', 'suspend', 'resume', 'tier_fulfillment', 'report_usage'],
                             0)

# The processor.py is the entry point of Processor execution
if __name__ == '__main__':

    # Reading the config.json file in the Processor
    config_file = Utils.get_config_file()
    # apiEndpoint is the API End-point of Connect
    connect_api_url = config_file['connectApiEndpoint'],
    # apiKey is the API key for authorization created in Integrations menu of Connect
    connect_key = config_file['connectApiKey'],
    # Products are the list of IDs of the products which needs to be processed by this Processor
    client = ConnectClient(api_key=connect_key[0], endpoint=connect_api_url[0])

    # If the Product has parameters of scope 'Tier' then Tier use case implementation will be required.
    # Make sure the project has the Tier use case included during project creation
    # The Tier Config Requests (TCR) needs to be processed first and then the corresponding Fulfillment Requests
    if hasattr(project_manager, 'tier_fulfillment'):
        # Filter to fetch the Tier-Config-Request (TCR) for this product
        # The processor needs to process only the TCRs in Pending status
        # TODO: Remove the 'inquiring' status from the filter query. It is added for the ease of debug and unit tests

        query_tcr = R()
        query_tcr &= R().configuration.product.id.oneof(Globals.PRODUCTS)
        query_tcr &= R().status.oneof(['pending', 'inquiring'])
        tc_requests = client.ns('tier').collection('config-requests').filter(query_tcr)
        # Process each TCR
        for tcr in tc_requests:
            project_manager.tier_fulfillment.TierConfiguration.process_request(tcr, client)

    # Filter to fetch all the subscription Fulfillment requests from Connect that need to be processed by this Processor
    query = R()
    query &= R().asset.product.id.oneof(Globals.PRODUCTS)
    query &= R().status.oneof(['pending'])

    # Applying the filter
    requests = client.collection('requests').filter(query)

    # Processing each request
    for request in requests:
        request_id = Utils.get_basic_value(request, 'id')
        request_status = Utils.get_basic_value(request, 'status')
        # Process all Fulfillment Request with status Pending
        if request_status == 'pending':
            # Check the type of Fulfillment Request
            request_type = Utils.get_basic_value(request, 'type')

            if request_type == 'purchase':
                # Type PURCHASE means, it is a new subscription in Connect
                if hasattr(project_manager, 'purchase'):
                    project_manager.purchase.Purchase.process_request(request, client)

            if request_type == 'change':
                # Type CHANGE means, it is a change request of an existing active subscription in Connect
                # Change request includes request for changing the quantity of subscribed item/SKU
                # or adding more items
                if hasattr(project_manager, 'change'):
                    project_manager.change.Change.process_request(request, client)

            if request_type == 'cancel':
                # Type CANCEL means, it is a cancel request to terminate an existing subscription in Connect
                if hasattr(project_manager, 'cancel'):
                    project_manager.cancel.Cancel.process_request(request, client)

            if request_type == 'suspend':
                # Type SUSPEND means, it is a suspend request of an existing active subscription in Connect
                if hasattr(project_manager, 'suspend'):
                    project_manager.suspend.Suspend.process_request(request, client)

            if request_type == 'resume':
                # Type RESUME means, it is a resume request of an existing suspended subscription in Connect
                if hasattr(project_manager, 'resume'):
                    project_manager.resume.Resume.process_request(request, client)

    # Check if the Usage use case is included in this project
    if hasattr(project_manager, 'report_usage'):
        # If the product contains items of type Pay-as-you-go the usage of such items needs to be submitted in Connect
        # Refer https://connect.cloudblue.com/community/modules/usage_module/ for more details about Usage in Connect

        # This usage can be submitted as per the desired frequency
        # Customize: Implement the logic for the required frequency of reporting Usage into Connect
        if datetime.today().day == Globals.DAY_TO_REPORT_USAGE:
            project_manager.report_usage.Usage(client).process_usage()
