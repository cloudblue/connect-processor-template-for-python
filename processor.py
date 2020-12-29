from connect.config import Config
from app.product_fulfillment import ProductFulfillment
from app.utils.utils import Utils
from app.utils.globals import Globals

# The processor.py is the entry point of Processor execution

if __name__ == '__main__':

    # Reading the config.json file in the Processor
    config_file = Utils.get_config_file()

    # Filtering and fetching the Fulfillment Request (PR-###-###-###-###) for the Product(s) from Connect
    fulfillment_automation = ProductFulfillment(Config(
        # apiEndpoint is the API End-point of Connect
        api_url=config_file['apiEndpoint'],
        # apiKey is the API key for authorization created in Integrations menu of Connect
        api_key=config_file['apiKey'],
        # products are the list of IDs of the products which needs to be processed by this Processor
        products=Globals.PRODUCTS
    ))

    # Constructing the filter to fetch the required Fulfillment Requests for Subscriptions
    fulfillment_filters = {'limit': 1000,
                           'status__in': 'pending',
                           'asset.product.id__in': ','.join(Globals.PRODUCTS),
                           'order_by': 'created',
                           'asset.connection.type': Globals.ENVIRONMENT}

    fulfillment_automation.process(fulfillment_filters)
