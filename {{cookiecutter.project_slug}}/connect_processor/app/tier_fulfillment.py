from connect_processor.app.utils.globals import Globals
from connect_processor.app.utils.utils import Utils

class TierConfiguration():

    # The purpose of the TCR is to get the details required for provisioning from the Reseller/Tier1
    # The Reseller receives an Activation form to submit the information

    def process_request(request, client):

        # Process the request for the tier.
        tcr_id = Utils.get_basic_value(request, 'id')
        tcr_status = Utils.get_basic_value(request, 'status')


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

        update_tier_parameter = Utils.update_Tier1_parameters(tcr_id, payload, client)

        # Update the status to Approved
        # The status will not get updated to Approved if any required/mandatory parameter is empty
        # Get the template
        product = Utils.get_value(request, 'configuration', 'product')
        product_id = Utils.get_basic_value(product, 'id')
        # Customize: Change the template name to match with the name configured in Product in Connect
        template_id = Utils.get_template_by_product(product_id, 'Default Activation Template', 'tier1', client)
        payload1 = {
            "template": {
                "id": template_id
            }
        }
        result = Utils.approve_Tier_config_request(tcr_id, payload1, client)
        return result



