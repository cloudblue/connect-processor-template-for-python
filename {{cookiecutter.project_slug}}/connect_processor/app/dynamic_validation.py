from flask import Flask, request, json



api = Flask(__name__)

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

@api.route('/validate', methods=['POST'])
def do_validate():

        data = request.json
        params = data['asset']['params']

        param_1 = get_parameter_by_id(params, 'param_dynamic_validation')
        param_1['value_error'] = 'This error is from the validation script!'
        params = set_parameter(params, param_1)

        data['asset']['params'] = params
        return data


