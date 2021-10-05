# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#

from flask import Flask, request
from connect_processor.app.utils.utils import Utils

api = Flask(__name__)

"""
# TO execute on local
set FLASK_APP=service
flask run
"""


def set_parameter(params, param):
    ret = []
    for p in params:
        if p['id'] == param['id']:
            ret.append(param)
        else:
            ret.append(p)
    return ret


# The webhook configured in Connect will call the validate method to validate the value provided as ordering
# parameter during order placement
@api.route('/validate', methods=['POST', 'GET'])
def do_validate():
    json_data = request.json
    # Customize: replace 'param_id_to_validate' with Id of the parameter that requires to be validated
    value = Utils.get_param_value(json_data, 'ordering', 'param_id_to_validate')
    # Customize: Implement the desired logic to validate the value provided as the parameter
    # api_client = APIClient(api_url='',
    #                        api_key='')
    # error_message = api_client.validate_param(value)

    # Customize: Provide proper error message
    error_message = "Param param_id_to_validate not valid "
    if len(error_message) > 0:
        params = json_data['asset']['params']
        validated_param = Utils.get_item_by_id(params, 'param_id_to_validate')
        validated_param['value_error'] = error_message
        set_parameter(params, validated_param)
    return json_data
