# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#

class APIClient(object):
    access_token = None
    authorization_header = None

    # API constructor.
    def __init__(self, api_url, api_key):
        self.type = ''
        self.api_url = api_url
        self.api_key = api_key

    def authenticated(self):
        # TODO: Complete the self.authorization_header with Authorization info
        self.authorization_header = {'Content-Type': 'application/json'}

    def create_subscription(self, data):
        # TODO: Implement create_subscription(data) method
        raise NotImplementedError

    def change_subscription(self, data, subscription_id):
        # TODO: Implement change_subscription(data, subscription_id) method
        raise NotImplementedError

    def cancel_subscription(self, data, subscription_id):
        # TODO: Implement cancel_subscription(data, subscription_id) method
        raise NotImplementedError

    def suspend_subscription(self, data, subscription_id):
        # TODO: Implement suspend_subscription(data, subscription_id) method
        raise NotImplementedError

    def resume_subscription(self, data, subscription_id):
        # TODO: Implement resume_subscription(data, subscription_id) method
        raise NotImplementedError

    def get_usage_records(self, data):
        # TODO: Implement get_usage_records(data) method
        raise NotImplementedError

    def check_reseller(self, data):
        # TODO: Implement check_reseller(data) method
        raise NotImplementedError
