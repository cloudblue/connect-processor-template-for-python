class Globals:

    # Global Constants

    PRODUCTS = ['PRD-###-###-###']
    SUBSCRIPTION_APPROVED_TEMPLATE = 'TTL-###-###-###'
    T1_APPROVED_TEMPLATE = 'TL-###-###-###'
    ENVIRONMENT = 'preview'
    
    DAY_TO_REPORT_USAGE = '#'

    ROOT_PATH_LOG = "rootPathLog"
    SUBSCRIPTION_UPDATED = 'SUBSCRIPTION_UPDATED'

    # Processing steps
    # SUBSCRIPTION_APPROVED_TEMPLATE = 'SUBSCRIPTION_APPROVED_TEMPLATE'


    # ACTIONS
    INQUIRE_ACTION = '<<< INQUIRE ACTION >>> '
    SKIP_ACTION = '<<< SKIP ACTION >>> '
    FAIL_ACTION = '<<< FAIL ACTION >>> '

    # LOGGER
    LOG_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    RESTRICTED_KEYS = ['CLIENT_SECRET',
                       'CLIENT_ID',
                       'REFRESH_TOKEN',
                       'ACCESS_TOKEN',
                       'ID_TOKEN',
                       'CODE',
                       'AUTHORIZATION',
                       'APPLICATIONID',
                       'APPLICATIONSECRET',
                       'REFRESHTOKEN',
                       'PASSWORD',
                       'PARTNER_CLIENT_SECRET',
                       'PARTNER_ACCESS_CODE',
                       'CLIENTID',
                       'CLIENTSECRET',
                       'USERNAME',
                       'BILLINGADDRESSID',
                       'BILLINGADDRESSNAME',
                       'PURCHASEORDERNUMBER',
                       'ID']
