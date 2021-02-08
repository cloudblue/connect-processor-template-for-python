from cnct import ConnectClient
import sys
import os
from connect_processor.app.utils.globals import Globals
from connect_processor.app.utils.utils import get_basic_value, Utils
from cnct import R
project_manager = __import__('connect_processor.app', globals(), locals(), [''], 0)



# The processor.py is the entry point of Processor execution

if __name__ == '__main__':

    # Reading the config.json file in the Processor
    config_file = Utils.get_config_file()
    # apiEndpoint is the API End-point of Connect
    connect_api_url = config_file['connectApiEndpoint'],
    # apiKey is the API key for authorization created in Integrations menu of Connect
    connect_key = config_file['connectApiKey'],
    # products are the list of IDs of the products which needs to be processed by this Processor
    client = ConnectClient(api_key=connect_key[0], endpoint=connect_api_url[0])

    query = R()
    query &= R().asset.product.id.oneof(Globals.PRODUCTS)
    query &= R().status.oneof(['pending'])

    project_manager = __import__('connect_processor.app', globals(), locals(),
                                 ['purchase', 'change', 'cancel', 'suspend', 'resume'], 0)

    requests = client.requests.filter(query)
    for request in requests:
        request_id = get_basic_value(request, 'id')
        type = get_basic_value(request, 'type')

        if type == 'purchase':
            # Type PURCHASE means, it is a new subscription in Connect
            if bool(project_manager.purchase):
                project_manager.purchase.Purchase.process_request(request, client)

        if type == 'change':
            # Type CHANGE means, it is a change request of an existing active subscription in Connect
            # Change request includes request for changing the quantity of subscribed item/SKU
            # or adding more items
            if bool(project_manager.change):
                project_manager.change.Change.process_request(request, client)

        if type == 'cancel':
            # Type CANCEL means, it is a cancel request to terminate an existing subscription in Connect
            if bool(project_manager.cancel):
                project_manager.cancel.Cancel.process_request(request, client)

        if type == 'suspend':
            # Type SUSPEND means, it is a suspend request of an existing active subscription in Connect
            if bool(project_manager.suspend):
                project_manager.suspend.Suspend.process_request(request, client)

        if type == 'resume':
            # Type RESUME means, it is a resume request of an existing suspended subscription in Connect
            if bool(project_manager.resume):
                project_manager.resume.Resume.process_request(request, client)
