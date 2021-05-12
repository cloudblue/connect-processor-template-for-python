# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#
class Globals:
    """ Global Constants.
        It is needed to customize the following:
        PRODUCTS: Connect own Product ID codes (separated by "," if many), of the requests to process
        ENVIRONMENT: preview for test purposes or production when it is ready and installed.
        DAY_TO_REPORT_USAGE : if this processor supports the Usage Report use-case,
            is the day of each month to submit the usage data for PPU items to Connect.
            For example, set DAY_TO_REPORT_USAGE = 1 to send the report the first day of each month.

        Here can be customized the name of the product templates to approve product requests.
    """

    PRODUCTS = ['PRD-###-###-###']
    ENVIRONMENT = 'preview'
    DAY_TO_REPORT_USAGE = '#'

    ACTIVATION_TEMPLATE_NAME = 'Default Activation Template'
    TIER_CONFIG_ACTIVATION_TEMPLATE_NAME = 'Default Activation Template'
