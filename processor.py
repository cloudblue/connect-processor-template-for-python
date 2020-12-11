import copy
import logging

from connect.config import Config
from connect.rql import Query
from app.product_fulfillment import ProductFulfillment
from app.utils.utils import Utils
from connect.logger import logger
from logging import FileHandler

# The processor.py is the entry point of Processor execution

def _set_custom_logger(*args):
    handlers = [copy.copy(hdlr) for hdlr in logger.handlers]
    log_level = logger.level
    logger.setLevel(log_level)
    logger.propagate = False
    logger.handlers = handlers
    info = " ".join(args)
    sformat = f"%(asctime)s %(levelname)-6s{info} >>> %(module)s -> %(funcName)s:LINE-%(lineno)d: %(message)s "
    [handler.setFormatter(logging.Formatter(sformat, "%Y-%m-%d %H:%M:%S"))
     for handler in logger.handlers]


if __name__ == '__main__':

    # Reading the config.json file in the Processor
    config_file = Utils.get_config_file()
    # Setting up Logging
    logger.setLevel(config_file["logLevel"])
    logger.addHandler(FileHandler("logs/ExampleProcessor.log"))
    _set_custom_logger()

    # Filtering and fetching the Purchase Request (PR-###-###-###-###) for the subscription from Connect
    fulfillment_automation = ProductFulfillment(Config(
        # apiEndpoint is the API End-point of Connect
        api_url=config_file['apiEndpoint'],
        # apiKey is the API key for authorization created in Integrations menu of Connect
        api_key=config_file['apiKey'],
        # products are the list of IDs of the products which needs to be processed by this Processor
        products=config_file['products']
    ))

    # Constructing the filter to fetch the required Fulfilment requests for Subscriptions
    fulfillment_filters = {'limit': 1000,
                           'status__in': 'pending',
                           'asset.product.id__in': ','.join(config_file['products']),
                           'order_by': 'created',
                           'asset.connection.type': config_file['service']['environment']}

    fulfillment_automation.process(fulfillment_filters)