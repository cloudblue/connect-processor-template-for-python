class TierFulfillmentMessages(object):
    RROR_PROCESSING_TIER_REQUEST = 'There has been an error processing the tier config request. Error description: {}'

class BasePurchaseMessages:
    pass


class BaseChangeMessages:
    pass


class BaseSuspendMessages:
    NOTHING_TO_DO = 'Suspend method for request {} - Nothing to do'


class BaseCancelMessages:
    ACTIVATION_TILE_RESPONSE = 'Operation cancel done successfully'

class BaseSharedMessages:
    ACTIVATING_TEMPLATE_ERROR = 'There has been a problem activating the template. Description {}'
    EMPTY_ACTIVATION_TILE = 'Activation tile response for marketplace {} cannot be empty'
    ERROR_GETTING_CONFIGURATION = 'There was an exception while getting configured info for the specified ' \
                                  'marketplace {}'
    NOT_FOUND_TEMPLATE = 'It was not found any template of type <{}> for the marketplace with id <{}>. ' \
                         'Please review the configuration.'
    NOT_ALLOWED_DOWNSIZE = 'At least one of the requested items at the order is downsized which ' \
                           ' is not allowed. Please review your order.'
    RESPONSE_ERROR = 'Error: {} -> {}'
    RESPONSE_DOES_NOT_HAVE_ATTRIBUTE = 'Response does not have attribute {}. Check your request params. ' \
                                       'Response status - {}'
    WAITING_SUBSCRIPTION_ACTIVATION = 'The subscription has been updated, waiting Vendor/ISV to update the ' \
                                            'subscription status'

class Message:
    class Shared(BaseSharedMessages):
        tier_request = TierFulfillmentMessages()

    class Purchase(BasePurchaseMessages):
        FAIL_REPEATED_PRODUCTS = 'It has been detected repeated products for the same purchase. ' \
                                 'Please review the configured plan.'

    class Change(BaseChangeMessages):
        pass

    class Suspend(BaseSuspendMessages):
        pass

    class Cancel(BaseCancelMessages):
        pass



