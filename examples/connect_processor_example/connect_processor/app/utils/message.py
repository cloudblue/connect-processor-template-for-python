class Message:

    RESPONSE_ERROR = 'Error: {} -> {}'
    PROCESSING_REQUEST_ERROR = 'Error while processing request - {}'
    RESPONSE_DOES_NOT_HAVE_ATTRIBUTE = 'Response does not have attribute {}. Check your request params. ' \
                                       'Response status - {}'