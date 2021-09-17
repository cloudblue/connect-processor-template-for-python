# -*- coding: utf-8 -*-
#
# Copyright (c) {% now 'utc', '%Y' %}, {{ cookiecutter.author }}
# All rights reserved.
#

from flask import Flask, request, json

api = Flask(__name__)

"""
# TO execute on local
set FLASK_APP=service
flask run
"""


def get_parameter_by_id(params, param_id):
    for param in params:
        if param['id'] == param_id:
            return param
    raise Exception('Parameter {id} not found.'.format(id=param_id))


def set_parameter(params, param):
    ret = []
    for p in params:
        if p['id'] == param['id']:
            ret.append(param)
        else:
            ret.append(p)
    return ret


def get_validation_request_data(request):
    data = request.data.decode("utf-8")
    json_data = json.loads(data)
    return json_data


# The webhook configured in Connect will call the validate method to validate the value provided as ordering
# parameter during order placement
@api.route('/validate', methods=['POST', 'GET'])
def do_validate():
    json_data = get_validation_request_data(request)
    params = json_data['asset']['params']
    # Customize: replace 'param_dynamic_validation' with Id of the parameter that requires to be validated
    param_1 = get_parameter_by_id(params, 'param_dynamic_validation')
    # Customize: Implement the desired logic to validate the value provided as the parameter
    if param_1 and param_1['value'].isnumeric():
        return api.response_class(
            response=json.dumps(json_data),
            status=200,
            mimetype='application/json'
        )

    else:
        # Customize: Provide proper error message
        param_1['value_error'] = "This error is from the validation script! Value should be numeric."
        params = set_parameter(params, param_1)
        json_data['asset']['params'] = params
        response = json.dumps(json_data)
        return api.response_class(
            response=response,
            status=200,
            mimetype='application/json'
        )
