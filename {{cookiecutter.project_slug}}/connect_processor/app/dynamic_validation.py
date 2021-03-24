
from flask import Flask, request, json

api = Flask(__name__)

"""
# TO execute on local
set FLASK_APP=service
flask run
"""

def get_parameter_by_id(params, id):
    for param in params:
        if param['id'] == id:
            return param
    raise Exception('Parameter {id} not found.'.format(id=id))


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
    jsondata = json.loads(data)
    return jsondata


# The webhook cofigured in Connect will call the validate method to validate the value provided as ordering parameter during order placement
@api.route('/validate', methods=['POST', 'GET'])
def do_validate():

    jsondata = get_validation_request_data(request)
    params = jsondata['asset']['params']
    # Customize: replace 'param_dynamic_validation' with Id of the parameter that requires to be validated
    param_1 = get_parameter_by_id(params, 'param_dynamic_validation')
    # Customize: Implement the desired logic to validate the value provided as the parameter
    if param_1 and param_1['value'].isnumeric():
        return api.response_class(
            response=json.dumps(jsondata),
            status=200,
            mimetype='application/json'
        )

    else:
        # Customize: Provide proper error message
        param_1['value_error'] = "This error is from the validation script! Value should be numeric."
        params = set_parameter(params, param_1)
        jsondata['asset']['params'] = params
        response = json.dumps(jsondata)
        return api.response_class(
            response=response,
            status=400,
            mimetype='application/json'
        )



