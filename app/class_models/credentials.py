# -*- coding: utf-8 -*-

from connect.exceptions import SkipRequest
from connect.models import Configuration
from app.exceptions.exceptions import CredentialsException


class Credentials:
    """ Parameters are used in product and asset definitions. """

    def __init__(self, marketplace_id, configuration: Configuration, environment, api_url, api_key):

        # Here there are 2 options to save the Vendor API access details
        # Customize as per choice

        try:
            self.marketplace = marketplace_id


            # Option 1 : Vendor API access details are configured in config.json file in this Processor
            if api_url and api_key:
                self.api_url = api_url
                self.api_key = api_key
            else:
                raise CredentialsException(
                    "Error API Credentials: api_url and api_key not found in the config file for marketplace {} ".format(marketplace_id))

            # Option 2 : Vendor API access details are configured in configuration parameters in Connect Product
            # self.api_url = configuration.get_param_by_id("api_url").value
            # self.api_key = configuration.get_param_by_id("api_key").value


        except CredentialsException as ex:
            raise SkipRequest(f"There was a problem retrieving API credentials for marketplace {marketplace_id}. "
                              f"Please review configured credentials in vendor portal for marketplace "
                              f"{marketplace_id}. Error >>> {str(ex)}")



