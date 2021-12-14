# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Carolina Giménez Escalante
# All rights reserved.
#
from connect.eaas.extension import (
    Extension,
    ProcessingResponse
)

from connect_ext.app.cancel import Cancel
from connect_ext.app.change import Change
from connect_ext.app.purchase import Purchase
from connect_ext.app.resume import Resume
from connect_ext.app.suspend import Suspend
from connect_ext.utils.utils import Utils


class ConnectExtensionProcessorExampleExtension(Extension):

    def process_asset_purchase_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        if request['status'] == 'pending':
            Utils.ACTIVATION_TEMPLATE_NAME = self.config['ACTIVATION_TEMPLATE_NAME']
            Utils.API_ENDPOINT = self.config['API_ENDPOINT']
            Purchase().process_request(request, self.client)
        return ProcessingResponse.done()

    def process_asset_change_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        if request['status'] == 'pending':
            Utils.ACTIVATION_TEMPLATE_NAME = self.config['ACTIVATION_TEMPLATE_NAME']
            Utils.API_ENDPOINT = self.config['API_ENDPOINT']
            Change().process_request(request, self.client)
        return ProcessingResponse.done()

    def process_asset_suspend_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        if request['status'] == 'pending':
            Utils.ACTIVATION_TEMPLATE_NAME = self.config['ACTIVATION_TEMPLATE_NAME']
            Utils.API_ENDPOINT = self.config['API_ENDPOINT']
            Suspend().process_request(request, self.client)
        return ProcessingResponse.done()

    def process_asset_resume_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        if request['status'] == 'pending':
            Utils.ACTIVATION_TEMPLATE_NAME = self.config['ACTIVATION_TEMPLATE_NAME']
            Utils.API_ENDPOINT = self.config['API_ENDPOINT']
            Resume().process_request(request, self.client)
        return ProcessingResponse.done()

    def process_asset_cancel_request(self, request):
        self.logger.info(f"Obtained request with id {request['id']}")
        if request['status'] == 'pending':
            Utils.ACTIVATION_TEMPLATE_NAME = self.config['ACTIVATION_TEMPLATE_NAME']
            Utils.API_ENDPOINT = self.config['API_ENDPOINT']
            Cancel().process_request(request, self.client)
        return ProcessingResponse.done()
