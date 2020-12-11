from connect.models.configuration import Param, Configuration

from connect.exceptions import SkipRequest, InquireRequest, FailRequest
from connect.resources.fulfillment import FulfillmentResource
from connect.config import Config
from app.class_models.credentials import Credentials
from app.utils.logger import logger
from app.utils.message import Message
from app.utils.globals import Globals
import json
from copy import deepcopy
from typing import Any, Dict

class Utils:
    # Actions
    VALIDATE_ACTION = 'validate'
    CREATE_ACTION = 'creation'
    CHANGE_ACTION = 'change'

    # Use this method if Vendor API access details will be configured in Connect as Configuration parameters in the Product
    @staticmethod
    def get_credentials(marketplace_id, configuration: Configuration, environment) -> Credentials:
        logger.info('Getting credentials for marketplace {}'.format(marketplace_id))
        try:
            config_file = Utils.get_config_file()
            api_url = config_file['service']['partnerConfig'][marketplace_id]['apiUrl']
            api_key = config_file['service']['partnerConfig'][marketplace_id]['apiKey']
            credentials = Credentials(marketplace_id=marketplace_id, configuration=configuration,
                                      environment=environment, api_url=api_url, api_key=api_key)
        except SkipRequest as err:
            raise err
        except Exception:
            message = Message.Shared.ERROR_GETTING_CONFIGURATION.format(marketplace_id)
            raise SkipRequest(message)

        return credentials

    @staticmethod
    def get_config_file() -> Dict[str, Any]:
        with open('./config.json') as file_handle:
            config = json.load(file_handle)
        return config

    @staticmethod
    def serialize(data, restrict=False):
        """Convert given object to printable structure
        Args:
            data: Generic object to be converted in string with json structure
            :param data: data to be converted
            :param restrict: hide sensitive data
        """
        dumped = json.dumps(data, default=lambda o: getattr(o, '__dict__', str(o)), check_circular=False)
        return Utils.drop_restricted_data(json.loads(dumped)) if restrict else json.loads(dumped)

    @staticmethod
    def drop_restricted_data(param):
        params = deepcopy(param)
        if params and isinstance(params, dict):
            for param_key in params.keys():
                if str(param_key).upper() in Globals.RESTRICTED_KEYS:
                    params[param_key] = "####-###-####"
                elif params[param_key] and isinstance(params[param_key], dict):
                    params[param_key] = Utils.drop_restricted_data(params[param_key])

        return params

    @staticmethod
    def is_null_or_empty(value):
        return value is None or value == 0 or len(value) == 0

    @staticmethod
    def get_status_code(info):
        return info['statusCode'] if 'statusCode' in info else ''

    @staticmethod
    def get_activation_template(configuration, template_type, marketplace_id):
        template_id = ""

        try:
            logger.info(f"Trying to get '{template_type}' for marketplace {marketplace_id}")
            # Getting the Activation Template provided in configuration parameter of Product in Connect
            if hasattr(configuration.get_param_by_id(template_type), 'value') and not Utils.is_null_or_empty(
                    configuration.get_param_by_id(template_type).value):
                template_id = configuration.get_param_by_id(template_type).value
            # Activation Template can be configured in config.json file in this Processor for a particular marketplace.
            # Customize this method accordingly to get the Activation Template ID from the config.json as desired.
            else:
                error_message = Message.Shared.NOT_FOUND_TEMPLATE.format(template_type,
                                                                         marketplace_id)
                logger.error(Globals.SKIP_ACTION + error_message)
                raise SkipRequest(error_message)
        finally:
            return template_id

    @staticmethod
    def is_downsize_request(items):
        for item in items:
            if item.old_quantity > item.quantity:
                return True

        return False

    @staticmethod
    def check_previous_active_subscription(filter):
        logger.debug("Checking if this customer already has a subscription")
        config_file = Utils.get_config_file()
        fulfilment_resource = FulfillmentResource(Config(
            api_url=config_file['apiEndpoint'],
            api_key=config_file['apiKey'],
            products=config_file['products']
        ))
        return fulfilment_resource.search_asset_request(filter)