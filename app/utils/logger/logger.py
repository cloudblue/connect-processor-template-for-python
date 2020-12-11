import json
import logging
import os
from copy import deepcopy
from functools import wraps
from logging import FileHandler
from typing import Any, Dict

from connect.models import BaseModel, Fulfillment, UsageFile, TierConfigRequest, UsageListing

from app.utils.globals import Globals


logger = logging.getLogger('connect')

def get_config_file() -> Dict[str, Any]:
    with open('./config.json') as file_handle:
        config = json.load(file_handle)
    return config

config_file = get_config_file()
root_path_log = config_file['service'][Globals.ROOT_PATH_LOG]
if os.path.exists(root_path_log) is False:
    os.mkdir(root_path_log)

if logger.handlers.__len__() == 0:
    logger.addHandler(logging.StreamHandler())
if len(list(filter(lambda hand: type(hand).__name__ == 'StreamHandler', logger.handlers))) > 0:
    sformat = f"%(asctime)s %(levelname)-6s| %(module)s (line %(lineno)d) => %(message)s"
    console_handler = list(filter(lambda hand: type(hand).__name__ == 'StreamHandler', logger.handlers))[0]
    console_handler.setFormatter(logging.Formatter(sformat, Globals.LOG_DATETIME_FORMAT))


def log_request_data(args):
    global logger
    if len(args) and isinstance(args[0], BaseModel):
        sformat = define_format(args[0])

        if isinstance(args[0], Fulfillment) or isinstance(args[0], UsageFile) or isinstance(args[0], UsageListing) \
                or isinstance(args[0], TierConfigRequest):
            file_handler = create_file_handler(args[0])

            for handler in logger.handlers:
                if hasattr(handler, 'baseFilename'):
                    logger.removeHandler(handler)

            logger.addHandler(file_handler)

        for handler in logger.handlers:
            handler.setFormatter(logging.Formatter(sformat, Globals.LOG_DATETIME_FORMAT))

    logger.propagate = False
    logger.disabled = False


def define_format(arg):
    sformat = ""
    info = ""
    if isinstance(arg, Fulfillment):
        info = info + arg.asset.id
    elif isinstance(arg, TierConfigRequest):
        info = info + arg.configuration.id
    info = info + " " + arg.id
    sformat = f"%(asctime)s >>> {info} %(levelname)-6s| %(module)s (line %(lineno)d) => %(message)s"

    return sformat


def create_file_handler(arg):
    if isinstance(arg, Fulfillment):
        log_folder = (root_path_log + "/" +
                      arg.asset.connection.provider.id + "/" +
                      arg.asset.connection.hub.id + "/" +
                      arg.asset.marketplace.id + "/" +
                      arg.asset.product.id)
        os.makedirs(log_folder, exist_ok=True)
        file_handler = FileHandler(log_folder + '/' + arg.asset.tiers.customer.id + '.log', 'a', 'utf-8')

    elif isinstance(arg, TierConfigRequest):
        log_folder = (root_path_log + "/" +
                      arg.configuration.connection.provider.id + "/" +
                      arg.configuration.connection.hub.id + "/" +
                      arg.configuration.marketplace.id + "/" +
                      arg.configuration.product.id)
        os.makedirs(log_folder, exist_ok=True)
        file_handler = FileHandler(log_folder + '/' + arg.configuration.account.id + '.log', 'a', 'utf-8')
    else:
        file_handler = FileHandler(root_path_log+'/connect_log.log', 'a', 'utf-8')

    return file_handler


def function_log(func):
    @wraps(func)
    def decorator(self, *args, **kwargs):
        log_request_data(args)
        if args.__len__() > 0 or kwargs.__len__() > 0:
            logger.debug(
                '>>> Entering `{}:{}` >>> PARAMS >>> {} {}'.format(func.__module__, func.__name__, serialize(args),
                                                             drop_restricted_data(serialize(kwargs))))
        else:
            logger.debug('>>> Entering `{}:{}`'.format(func.__module__, func.__name__))
        result = func(self, *args, **kwargs)
        if result is not None:
            logger.debug(
                '<<< Function `{}.{}` <<< RETURN: <<< {}'.format(self.__class__.__name__, func.__name__, drop_restricted_data(serialize(result))))
        return result

    return decorator


def serialize(data):
    """Convert given object to printable structure
    Args:
        data: Generic object to be converted in string with json structure
    """
    dumped = json.dumps(data, default=lambda o: getattr(o, '__dict__', str(o)))
    return json.loads(dumped)

def drop_restricted_data(param):
    params = deepcopy(param)
    if params and isinstance(params, dict):
        for param_key in params.keys():
            if str(param_key).upper() in Globals.RESTRICTED_KEYS:
                params[param_key] = "####-###-####"
            elif params[param_key] and isinstance(params[param_key], dict):
                params[param_key] = drop_restricted_data(params[param_key])

    return params

