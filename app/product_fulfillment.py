import re
from connect.resources import FulfillmentAutomation
from datetime import datetime
from app.api_client.isv_client import APIClient
from app.utils.utils import Utils
from app.utils.globals import Globals
from connect.exceptions import FailRequest, SkipRequest, InquireRequest
from app.utils.message import Message
from connect.models import Param, ActivationTemplateResponse, Fulfillment, ActivationTileResponse


class ProductFulfillment(FulfillmentAutomation):

    # This method processes the Fulfillment Requests in Pending status for all the actions
    # Returns Activation response to Connect which updates the status of Fulfillment Request as well as Subscription

    def process_request(self, req: Fulfillment) -> object:
        # The req, parameter of process_request, is an object for Fulfilment Request for the Subscription in Connect
        try:

            # Checking the type of Subscription from Connect
            if req.type == 'purchase':
                # Type PURCHASE means, it is a new subscription in Connect
                return self.purchase(req=req, automation=self)
            if req.type == 'change':
                # Type CHANGE means, it is a change request of an existing active subscription in Connect
                # Change request includes request for changing the quantity of subscribed item/SKU
                # or adding more items
                return self.change(req=req, automation=self)
            if req.type == 'suspend':
                # Type SUSPEND means, it is a suspend request of an existing active subscription in Connect
                return self.suspend(req=req, automation=self)
            if req.type == 'resume':
                # Type RESUME means, it is a resume request of an existing suspended subscription in Connect
                return self.resume(req=req, automation=self)
            if req.type == 'cancel':
                # Type CANCEL means, it is a cancel request of an existing subscription in Connect
                return self.cancel(req=req, automation=self)


        except SkipRequest as err:
            raise err
        except FailRequest as err:
            raise err

    # This method processes the Fulfillment Request for creating new subscription
    # Returns Activation response template configured in Connect and updates the status of Fulfilment Request as well as Subscription
    def purchase(self, req, automation: FulfillmentAutomation):

        # Validate Ordering parameters.
        # Ordering parameters could be used in API payload to create subscription in Vendor system.
        # self.check_order_parameters(req)
        # If validation fails, this method can raise Inquire request with appropriate message to get proper information.

        # If validation is successful then proceed

        # If the customer creation action or API is separate from subscription creation, then introduce a method for customer creation.
        # self.create_customer(req)

        # Create subscription
        subscription_info = self._create_subscription(automation, req)

        # If none of the SkipRequest, InquireRequst or FailRequest was raised, means that the provisioning was successful.
        # Approve the Fulfilment request by returning the Activation template
        # Approved is the final status of the Fulfilment Request of Subscription in Connect
        try:
            return ActivationTemplateResponse(Globals.ACTIVATION_TEMPLATE)
            # Returning the Activation Template will update the status of Fulfilment Request to Approved and Subscription status to Active.

            # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfilment Request remain empty.

        except SkipRequest as skip:
            raise skip
        except FailRequest as err:

            # The Fulfillment Request was provisioned successfully, but Activation template could not be returned successfully.
            # Therefore, we log the error message and do not fail the request
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(err.message)))
        except Exception as ex:
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(ex)))

    # This method is responsible to make the Vendor API calls to create the subscription
    def _create_subscription(self, automation, req):

        try:
            # Preparing payload for Create Subscription Vendor API
            data = self._parse_subscription(req)

            # Get the Vendor API credentials.

            # The location to save Vendor API credentials can be as desired. Customize to fetch request accordingly
            config_file = Utils.get_config_file()

            # Initiating the API client
            api_client = APIClient(config_file['partnerConfig']['apiUrl'],config_file['partnerConfig']['apiKey'])

            # Send payload (request) to make the Vendor API call for creating subscription
            subscription_info = api_client.create_subscription(data=data)

            # Check if the API call was successful and save the response request in Connect
            # Change 'tenantId' with relevant key from your response json
            if subscription_info['tenantId']:

                # Save the info in the response as fulfilment parameters for Subscription in Connect

                # The id of param should match with the id of one of the Product's fulfilment parameter in Connect. Change the id accordingly
                params = [
                        Param(id='subscriptionId', value=subscription_info['tenantId'])
                ]
                # Update the fulfilment parameters in Fulfilment Request in Connect with the corresponding value
                automation.update_parameters(req.id, params)

            else:
                # If API call returned error, Raise the concerned action accordingly
                if subscription_info['errors'][0].get('errorCode') is None \
                        or subscription_info['errors'][0].get('errorCode') == 'UNKNOWN_ERROR':

                    # Since the error was unknown, the request will be skipped to be attempted again later
                    raise SkipRequest(subscription_info['errors'][0].get('errorMessage'))
                else:
                    # Fail the Fulfilment request and provide error message in API response
                    raise FailRequest(subscription_info['errors'][0].get('errorMessage'))

        except FailRequest as err:
            # Fail the Fulfilment request if any issue encountered in the above try block
            # Add proper validations and handle boundary and corner cases appropriately to avoid failure.
            raise err
        return subscription_info

    # This method is responsible to construct payload/body required to make the Vendor API call to create/change the subscription
    def _parse_subscription(self, req):

       # Preparing API payload/body json
        # The request needs to be as per the schema requirement of Vendor API

        data = {}

        # The following is the example of how to use request from req in the payload body
        # request = {
        #     "company": {
        #         "name": request.asset.tiers.customer.name,
        #         "address": request.asset.tiers.customer.contact_info.address_line1,
        #         "city": request.asset.tiers.customer.contact_info.city,
        #         "state": request.asset.tiers.customer.contact_info.state,
        #         "postal_code": request.asset.tiers.customer.contact_info.postal_code,
        #         "country": request.asset.tiers.customer.contact_info.country,
        #         "note": "",
        #         "emergency_email": request.asset.get_param_by_id('customer_admin_email').value
        #     },
        #     "user": {
        #         # "login_name": request.asset.get_param_by_id('login_name').value,
        #         "login_name": login_name,
        #         "first_name": request.asset.tiers.customer.contact_info.contact.first_name,
        #         "last_name": request.asset.tiers.customer.contact_info.contact.last_name,
        #         "phone": {
        #             "area_code": request.asset.tiers.customer.contact_info.contact.phone_number.area_code,
        #             "number": request.asset.tiers.customer.contact_info.contact.phone_number.phone_number,
        #             "extension": request.asset.tiers.customer.contact_info.contact.phone_number.extension
        #         },
        #         "email": request.asset.get_param_by_id('customer_admin_email').value,
        #         "time_zone": "Pacific Standard Time",
        #         "language": "en-US"
        #     }
        # }

        return data

    # This method processes the fulfilment request for updating existing subscription
    def change(self, req, automation: FulfillmentAutomation):

        # If the business does not support downsize, check if any item quantity is reduced.
        # If yes, fail the request with proper message.
        self.check_if_downsize(req)

        # Process the request to change the subscription
        self._change_subscription(automation, req)

        # If none of the SkipRequest, InquireRequst or FailRequest was raised, means that the provisioning was successful.
        # Approve the Fulfilment Request by sending back the Activation template
        # Approve is the final status of the Fulfilment Request

        try:
            # Returning the Activation Template will update the status of Fulfilment Request object to Approved and Subscription object status remains Active.
            # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfilment Request remain empty.
            return ActivationTemplateResponse(Globals.ACTIVATION_TEMPLATE)
            # If required, another template can be created and in Vendor Portal. Pass the Template Id to return the template.
        except SkipRequest as skip:
            raise skip
        except FailRequest as err:
            # The Fulfilment Request was provisioned successfully, but Activation template could not be returned successfully.
            # Therefore, we log the error message and do not fail the request
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(err.message)))
        except Exception as ex:
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(ex)))

    # This method checks if the change request is a downsize. If yes, fails the request. This can be a requirement if refund is not allowed.
    @staticmethod
    def check_if_downsize(req):
        if Utils.is_downsize_request(req.asset.items):
            raise FailRequest(Message.Shared.NOT_ALLOWED_DOWNSIZE)

    # This method is responsible to make the Vendor API calls to update a subscription
    def _change_subscription(self, automation, req):
        try:

            # Get the existing subscription Id saved as fulfilment parameter
            subscriptionId = req.asset.get_param_by_id('subscriptionId').value

            # Prepare the body/payload for the Vendor API to update the subscription
            data = self._parse_subscription(req=req)

            # Get the Vendor API credentials.

            # The location to save Vendor API credentials can be as desired. Customize to fetch request accordingly
            config_file = Utils.get_config_file()

            # Initiating the API client
            api_client = APIClient(config_file['partnerConfig']['apiUrl'], config_file['partnerConfig']['apiKey'])

            # Send payload (request) to make the Vendor API call for changing subscription
            operation_result = api_client.change_subscription(data, subscriptionId)

            # Check if the API call was successful and save the response request in Connect
            self._check_update_response(automation, operation_result, req)

        except FailRequest as err:
            raise err

    def _check_update_response(self, automation, operation_result, req):
        if Utils.get_status_code(operation_result).lower() == 'success':
            now = datetime.now()
            params = [
                      Param(id='creationDate', value=now),
                      ]
            automation.update_parameters(req.id, params)

        else:
            # If API call returned error, Raise the concerned action accordingly
            if "errors" in operation_result:
                if operation_result['errors'][0].get('errorCode') is None \
                        or operation_result['errors'][0].get('errorCode') == 'UNKNOWN_ERROR':
                    # Since the error was unknown, the request will be skipped to be attempted again later
                    raise SkipRequest(operation_result['errors'][0].get('errorMessage'))
                else:
                    # Fail the Fulfilment Request if any issue encountered in the above try block
                    # Add proper validations and handle boundary and corner cases appropriately to avoid failure.
                    raise FailRequest(message=operation_result['errors'][0].get('errorMessage'))
            else:
                if "error" in operation_result:
                    raise Exception(operation_result['error'])


    # This method processes the Fulfillment Request for cancelling a subscription
    def cancel(self, req, automation: FulfillmentAutomation):

        # Check if the subscription is Active

        cancelled_subscription = self._cancel_subscription(automation, req)

        # Check if the API call was successful and save the response request in Connect
        # Update fulfilment parameters in Fulfilment request with the request in the response from the Vendor API call. Similar to _check_update_response

        try:
            return ActivationTemplateResponse(Globals.ACTIVATION_TEMPLATE)
            # Returning the Activation Template will update the status of Fulfilment Request object to Approved and Subscription object status to Terminated.
            # The statuses will not get updated as Approved and Terminated if any of the mandatory/required fulfilment parameter in Fulfilment Request remain empty.

        except SkipRequest as skip:
            raise skip
        except FailRequest as err:
            # The Fulfilment Request was provisioned successfully, but Activation template could not be returned successfully.
            # Therefore, we log the error message and do not fail the request
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(err.message)))
        except Exception as ex:
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(ex)))

    # This method is responsible to make the Vendor API calls to cancel a subscription
    def _cancel_subscription(self, automation, req):
        try:

            # Get the subscription Id from the request that needs to be cancelled
            subscriptionId = req.asset.get_param_by_id('subscriptionId').value

            # Prepare the body/payload for the Vendor API to cancel the subscription
            data = self._parse_cancel(req)

            # Get the Vendor API credentials.

            # The location to save Vendor API credentials can be as desired. Customize to fetch request accordingly
            config_file = Utils.get_config_file()

            # Initiating the API client
            api_client = APIClient(config_file['partnerConfig']['apiUrl'], config_file['partnerConfig']['apiKey'])

            # Send payload (request) to make the Vendor API call for cancelling subscription
            operation_result = api_client.cancel_subscription(data, subscriptionId)

            return operation_result

        except FailRequest as err:
            raise err

    # This method is responsible to construct payload/body required to make the Vendor API call to cancel the subscription
    def _parse_cancel(self, req):

        # Preparing API payload/body json
        # The request needs to be as per the schema requirement of Vendor API

        # Customize and construct he JSON for cancel subscription operation as per the API schema
        data = {}
        return data


    # This method processes the fulfilment request for suspending a subscription
    def suspend(self, req, automation: FulfillmentAutomation):

        # Check if the subscription is Active

        suspended_subscription = self._suspend_subscription(automation, req)

        # Check if the API call was successful and save the response request in Connect
        # Update fulfilment parameters in Fulfilment request with the request in the response from the Vendor API call. Similar to _check_update_response

        try:
            return ActivationTemplateResponse(Globals.ACTIVATION_TEMPLATE)
            # Returning the Activation Template will update the status of Fulfilment Request object to Approved and Subscription object status to Suspended.
            # The statuses will not get updated as Approved and Suspended if any of the mandatory/required fulfilment parameter in Fulfilment Request remain empty.
            # Another template can be created in Vendor Portal. Pass the Template Id to use it.

        except SkipRequest as skip:
            raise skip
        except FailRequest as err:
            # The Fulfilment Request was provisioned successfully, but Activation template could not be returned successfully.
            # Therefore, we log the error message and do not fail the request
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(err.message)))
        except Exception as ex:
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(ex)))

    # This method is responsible to make the Vendor API calls to suspend a subscription
    def _suspend_subscription(self, automation, req):
        try:

            # Get the subscription Id from the request that needs to be suspended
            subscriptionId = None
            subscriptionId = req.asset.get_param_by_id('subscriptionId').value

            # Prepare the body/payload for the Vendor API to suspend the subscription
            data = self._parse_suspend(req)

            # Get the Vendor API credentials.

            # The location to save Vendor API credentials can be as desired. Customize to fetch request accordingly
            config_file = Utils.get_config_file()

            # Initiating the API client
            api_client = APIClient(config_file['partnerConfig']['apiUrl'], config_file['partnerConfig']['apiKey'])

            # Send payload (request) to make the Vendor API call for suspending subscription
            operation_result = api_client.suspend_subscription(data, subscriptionId)

            return operation_result

        except FailRequest as err:
            raise err

    # This method is responsible to construct payload/body required to make the Vendor API call to suspend the subscription
    def _parse_suspend(self, req):

        # Preparing API payload/body json
        # The request needs to be as per the schema requirement of Vendor API

        # Customize and construct he JSON for cancel subscription operation as per the API schema
        data = {}
        return data


    # This method processes the fulfilment request for resuming a subscription
    def resume(self, req, automation: FulfillmentAutomation):

        # Check if the subscription status is Suspended

        resumed_subscription = self._resume_subscription(automation, req)

        # Check if the API call was successful and save the response request in Connect
        # Update fulfilment parameters in Fulfilment request with the request in the response from the Vendor API call. Similar to _check_update_response

        try:
            return ActivationTemplateResponse(Globals.ACTIVATION_TEMPLATE)
            # Returning the Activation Template will update the status of Fulfilment Request object to Approved and Subscription object status to Active.
            # The statuses will not get updated as Approved/Active if any of the mandatory/required fulfilment parameter in Fulfilment Request remain empty.

        except SkipRequest as skip:
            raise skip
        except FailRequest as err:
            # The Fulfilment Request was provisioned successfully, but Activation template could not be returned successfully.
            # Therefore, we log the error message and do not fail the request
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(err.message)))
        except Exception as ex:
            raise SkipRequest(Message.Shared.ACTIVATING_TEMPLATE_ERROR.format(str(ex)))

    # This method is responsible to make the Vendor API calls to resume a subscription
    def _resume_subscription(self, automation, req):
        try:

            # Get the subscription Id from the request that needs to be resumed
            subscriptionId = None
            subscriptionId = req.asset.get_param_by_id('subscriptionId').value

            # Prepare the body/payload for the Vendor API to resume the subscription
            data = self._parse_resume(req)

            # Get the Vendor API credentials.

            # The location to save Vendor API credentials can be as desired. Customize to fetch request accordingly
            config_file = Utils.get_config_file()

            # Initiating the API client
            api_client = APIClient(config_file['partnerConfig']['apiUrl'], config_file['partnerConfig']['apiKey'])

            # Send payload (request) to make the Vendor API call for resuming subscription
            operation_result = api_client.resume_subscription(data, subscriptionId)

            return operation_result

        except FailRequest as err:
            raise err

    # This method is responsible to construct payload/body required to make the Vendor API call to resume the subscription
    def _parse_resume(self, req):

        # Preparing API payload/body json
        # The request needs to be as per the schema requirement of Vendor API

        # Customize and construct he JSON for resume subscription operation as per the API schema
        data = {}
        return data


    def activate_template(self, req, template_type):

        # Get the Activation Template by the ID saved in the configuration parameter for a marketplace
        activation_response = ActivationTemplateResponse(
            Utils.get_activation_template(configuration=req.asset.configuration, marketplace_id=req.marketplace.id,
                                          template_type=template_type))
        if len(activation_response.template_id) == 0:
            raise SkipRequest(
                message=Message.Shared.EMPTY_ACTIVATION_TILE.format(req.marketplace.id))
        return activation_response

    def check_order_parameters(self, req: Fulfillment):
        # Validate to ensure the attempt to create subscription in Vendor System does not fail.
        # For Example - If an ordering parameter is configured to provide email, check if email matches regex
        # For example - If Vendor APIs include API to validate some request before creating subscription, call it.

        params = []
        error_msg = ''
        # Regular Expression to validate any type of value. For example, email
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        # Get the ordering parameter by ID
        # Ordering parameters are created in product in Connect Vendor Portal.
        email = req.asset.get_param_by_id('customer_admin_email').value

        # Check if request matches the regex
        if email:
            if (re.search(regex, email)):
                params.append(Param(id='customer_admin_email', value=email))
            else:
                error_msg = 'Please enter a valid customer admin email.'
        else:
            error_msg = 'Please enter customer admin email.'

        # If requirement is not fulfilled, change the status of the Fulfilment request of Subscription to Inquiring, as below
        if not all([
            hasattr(req.asset.get_param_by_id('customer_admin_email'), 'value')]
        ):
            raise InquireRequest(error_msg, params)