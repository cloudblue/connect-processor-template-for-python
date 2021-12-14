# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Carolina Giménez Escalante
# All rights reserved.
#
from unittest.mock import MagicMock, patch

from connect_ext.extension import ConnectExtensionProcessorExampleExtension


@patch('connect_ext.app.api_client.isv_client.APIClient.create_subscription',
       MagicMock(return_value={'tenantId': 3}))
@patch('connect_ext.app.api_client.isv_client.APIClient.change_subscription',
       MagicMock(return_value=''))
@patch('connect_ext.utils.utils.Utils._get_template_by_product',
       MagicMock(return_value='TA-###-###'))
def test_process_asset_purchase_request(
        sync_client_factory,
        response_factory,
        logger,
        ff_template,
        ff_request,
):
    config = {'ACTIVATION_TEMPLATE_NAME': '', 'API_ENDPOINT': ''}
    request = {'id': 1, 'status': 'pending', 'params': {}, 'asset': {'items': [{'quantity': 23, 'period': ''}]}}
    responses = [
        response_factory(value=ff_request, status=200),
        response_factory(value=ff_template, status=200),
        response_factory(value=ff_request, status=200),
    ]
    client = sync_client_factory(responses)
    ext = ConnectExtensionProcessorExampleExtension(client, logger, config)
    result = ext.process_asset_purchase_request(request)
    assert result.status == 'success'


@patch('connect_ext.app.api_client.isv_client.APIClient.change_subscription',
       MagicMock(return_value=''))
@patch('connect_ext.utils.utils.Utils._get_template_by_product',
       MagicMock(return_value='TA-###-###'))
def test_process_asset_change_request(
        sync_client_factory,
        response_factory,
        logger,
        ff_template,
        ff_request,
):
    config = {'ACTIVATION_TEMPLATE_NAME': '', 'API_ENDPOINT': ''}
    request = {'id': 1, 'status': 'pending', 'asset': {'items': [{'quantity': 23, 'period': ''}]}}
    responses = [
        response_factory(value=ff_template, status=200),
        response_factory(value=ff_request, status=200),
    ]
    client = sync_client_factory(responses)
    ext = ConnectExtensionProcessorExampleExtension(client, logger, config)
    result = ext.process_asset_change_request(request)
    assert result.status == 'success'


@patch('connect_ext.app.api_client.isv_client.APIClient.change_subscription',
       MagicMock(return_value=''))
@patch('connect_ext.utils.utils.Utils._get_template_by_product',
       MagicMock(return_value='TA-###-###'))
def test_process_asset_wrong_change_request(
        sync_client_factory,
        response_factory,
        logger,
        ff_template,
        ff_request,
):
    config = {'ACTIVATION_TEMPLATE_NAME': '', 'API_ENDPOINT': ''}
    request = {'id': 1, 'status': 'pending',
               'asset': {'items': [{'quantity': 23, 'period': ''}, {'quantity': 2, 'period': ''}]}}
    responses = [
        response_factory(value=ff_template, status=200),
        response_factory(value=ff_request, status=200),
    ]
    client = sync_client_factory(responses)
    ext = ConnectExtensionProcessorExampleExtension(client, logger, config)
    result = ext.process_asset_change_request(request)
    assert result.status == 'success'


@patch('connect_ext.app.api_client.isv_client.APIClient.suspend_subscription',
       MagicMock(return_value=''))
@patch('connect_ext.utils.utils.Utils._get_template_by_product',
       MagicMock(return_value='TA-###-###'))
def test_process_asset_suspend_request(
        sync_client_factory,
        response_factory,
        logger,
        ff_template,
        ff_request,
):
    config = {'ACTIVATION_TEMPLATE_NAME': '', 'API_ENDPOINT': ''}
    request = {'id': 1, 'status': 'pending', 'asset': {'items': [{'quantity': 23, 'period': 'OneTime'}]}}
    responses = [
        response_factory(value=ff_template, status=200),
        response_factory(value=ff_request, status=200),
    ]
    client = sync_client_factory(responses)
    ext = ConnectExtensionProcessorExampleExtension(client, logger, config)
    result = ext.process_asset_suspend_request(request)
    assert result.status == 'success'


@patch('connect_ext.app.api_client.isv_client.APIClient.resume_subscription',
       MagicMock(return_value=''))
@patch('connect_ext.utils.utils.Utils._get_template_by_product',
       MagicMock(return_value='TA-###-###'))
def test_process_asset_resume_request(
        sync_client_factory,
        response_factory,
        logger,
        ff_template,
        ff_request,
):
    config = {'ACTIVATION_TEMPLATE_NAME': '', 'API_ENDPOINT': ''}
    request = {'id': 1, 'status': 'pending'}
    responses = [
        response_factory(value=ff_template, status=200),
        response_factory(value=ff_request, status=200),
    ]
    client = sync_client_factory(responses)
    ext = ConnectExtensionProcessorExampleExtension(client, logger, config)
    result = ext.process_asset_resume_request(request)
    assert result.status == 'success'


@patch('connect_ext.app.api_client.isv_client.APIClient.cancel_subscription',
       MagicMock(return_value=''))
@patch('connect_ext.utils.utils.Utils._get_template_by_product',
       MagicMock(return_value='TA-###-###'))
def test_process_asset_cancel_request(
        sync_client_factory,
        response_factory,
        logger,
        ff_template,
        ff_request,
):
    config = {'ACTIVATION_TEMPLATE_NAME': '', 'API_ENDPOINT': ''}
    request = {'id': 1, 'status': 'pending', 'asset': {'items': [{'quantity': 23, 'period': ''}]}}
    responses = [
        response_factory(value=ff_template, status=200),
        response_factory(value=ff_request, status=200),
    ]
    client = sync_client_factory(responses)
    ext = ConnectExtensionProcessorExampleExtension(client, logger, config)
    result = ext.process_asset_cancel_request(request)
    assert result.status == 'success'
