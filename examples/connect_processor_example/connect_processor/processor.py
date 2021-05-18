from cnct import ConnectClient
from datetime import datetime
from examples.connect_processor_example.connect_processor.app.utils.globals import Globals
from examples.connect_processor_example.connect_processor.app.utils.utils import Utils
from cnct import R

project_manager = __import__('examples.connect_processor_example.connect_processor.app', globals(), locals(),
                             ['purchase', 'change', 'cancel', 'suspend', 'resume', 'tier_fulfillment', 'report_usage'],
                             0)


def process_request():
    try:
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

    except Exception as err:
        if len(err.args) > 0:
            Utils.save_error(client, Utils.get_basic_value(request, 'id'), err.args[0])
        raise err


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

    # Filter to fetch all the subscription Fulfillment requests from Connect that need to be processed by this Processor
    query = R()
    query &= R().asset.product.id.oneof(Globals.PRODUCTS)
    query &= R().status.oneof(['pending'])

    # Applying the filter
    requests = client.collection('requests').filter(query)

    # Processing each request
    for request in requests:
        process_request()
