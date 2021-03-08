from connect_processor.app.utils.globals import Globals
from connect_processor.app.utils import utils

class TierConfiguration():

    def process_request(request, client):

        # Process the request for the tier.
        # Update mandatory/required information in the parameters of scope tier.
        # Update the status to Approved
        request_id = 123
        payload = {"template_id": Globals.ACTIVATION_TEMPLATE_TIER}
        # result = client.requests[request_id]('approve').post(payload=payload)
