from connect_processor.app.utils.globals import Globals
from connect_processor.app.utils.utils import Utils, get_basic_value

class TierConfiguration():

    # The purpose of the TCR is to get the details required for provisioning from the Reseller/Tier1
    # The Reseller receives an Activation form to submit the information

    def process_request(request, client):

        # Process the request for the tier.
        tcr_id = get_basic_value(request, 'id')
        tcr_status = get_basic_value(request, 'status')


        # Updating the status of TCR from Inquiring to Pending
        # This step is not required in Production environment.
        # because this status gets updated from Inquiring to Pending when the Reseller/Tier1 submits the required information in the Activation form made available to him in the Commerce platform
        # Customize: Remove this step

        if tcr_status == 'inquiring':
            tcr_pending = client.ns('tier').collection('config_requests')[tcr_id]('pend').post(payload={})

        # Updating mandatory/required information in the parameters of scope tier.
        # This step is not required in Production environment.
        # Because this information will get updated when the Reseller fills in the information in the Activation form made available to them in a link in  Commerce Platform
        # Customize: Remove this step

        Info_for_tier = "Information from the reseller"
        payload = {
            "params": [{
                "id": "Info_for_tier",
                "value": Info_for_tier,
                "value_error": "",
                "structured_value": ""}]}

        update_tier_parameter = TierConfiguration.update_parameters(tcr_id, payload, client)

        # Update the status to Approved
        # The status will not get updated to Approved if any required/mandatory parameter is empty
        payload1 = {"template":{"id":Globals.T1_APPROVED_TEMPLATE}}
        result = TierConfiguration.approve_request(tcr_id, payload1, client)
        return result

    def update_parameters(tcr_id, payload, client):
        # This will update the value in the parameters in the fulfillment request
        tier_request = client.ns('tier').collection('config-requests')[tcr_id].update(payload=payload)
        return tier_request

    def approve_request(tcr_id, payload, client):
        # Approve the fulfillment request. The status of fulfillment request will be updated to Approved. And the status of Subscription will get updated to Active.
        result = client.ns('tier').collection('config-requests')[tcr_id]('approve').post(payload=payload)
        # result = client.requests[request_id].approve
        # purchase_result = result.post(payload=payload)
        return purchase_result
    def update_parameters(tcr_id, payload, client):
        # This will update the value in the parameters in the fulfillment request
        tier_request = client.ns('tier').collection('config-requests')[tcr_id].update(payload=payload)
        return tier_request

    def approve_request(tcr_id, payload, client):
        # Approve the fulfillment request. The status of fulfillment request will be updated to Approved. And the status of Subscription will get updated to Active.
        result = client.ns('tier').collection('config-requests')[tcr_id]('approve').post(payload=payload)
        # result = client.requests[request_id].approve
        # purchase_result = result.post(payload=payload)
        return purchase_result