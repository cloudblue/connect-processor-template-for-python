from cnct import ConnectClient
from datetime import datetime
from calendar import monthrange
from connect_processor.app.utils.globals import Globals
from connect_processor.app.utils.utils import get_basic_value, get_value, Utils
from connect_processor.app.report_usage import Usage
from cnct import R
project_manager = __import__('connect_processor.app', globals(), locals(),
                                 ['purchase', 'change', 'cancel', 'suspend', 'resume', 'tier_fulfillment'], 0)


# The processor.py is the entry point of Processor execution
if __name__ == '__main__':

    # Reading the config.json file in the Processor
    config_file = Utils.get_config_file()
    # apiEndpoint is the API End-point of Connect
    connect_api_url = config_file['connectApiEndpoint'],
    # apiKey is the API key for authorization created in Integrations menu of Connect
    connect_key = config_file['connectApiKey'],
    # products are the list of IDs of the products which needs to be processed by this Processor
    client = ConnectClient(api_key=connect_key[0], endpoint=connect_api_url[0])

    # Filter to fetch all the subscription Fulfillment requests from Connect that need to be processed by this Processor
    query = R()
    query &= R().asset.product.id.oneof(Globals.PRODUCTS)
    query &= R().status.oneof(['pending,tiers_setup'])

    # Applying the filter
    requests = client.requests.filter(query)

    # Processing each request
    for request in requests:
        request_id = get_basic_value(request, 'id')

        # Check if the Fulfillment Request has a Tier-Config-Request or TCR
        # If yes, the TCR needs to be processed first and then the corresponding Fulfillment Request
        request_status = get_basic_value(request, 'status')
        # The TCR needs to be processed only if the Fulfillment Request status is tiers_setup, which means some tier1/reseller information will be required
        if(request_status) == 'tiers_setup':
            if bool(project_manager.tier_fulfillment):
                tiers = get_value(request, 'asset', 'tiers')
                tier1_id = get_value(tiers, 'tier1', 'id')

                # Filter to fetch the corresponding TCR
                query_tcr = R()
                query_tcr &= R().Settings.requests.configuration.account.id.oneof([tier1_id])

                tcr = client('tier').config_requests.filter(query_tcr).first()

                # This will process the TCR
                project_manager.tier_fulfillment.TierConfiguration.process_request(tcr, client)

        # Check the type of Fulfillment Request
        type = get_basic_value(request, 'type')

        if type == 'purchase':
            # Type PURCHASE means, it is a new subscription in Connect
            if bool(project_manager.purchase):
                project_manager.purchase.Purchase.process_request(request, client)

        if type == 'change':
            # Type CHANGE means, it is a change request of an existing active subscription in Connect
            # Change request includes request for changing the quantity of subscribed item/SKU
            # or adding more items
            if bool(project_manager.change):
                project_manager.change.Change.process_request(request, client)

        if type == 'cancel':
            # Type CANCEL means, it is a cancel request to terminate an existing subscription in Connect
            if bool(project_manager.cancel):
                project_manager.cancel.Cancel.process_request(request, client)

        if type == 'suspend':
            # Type SUSPEND means, it is a suspend request of an existing active subscription in Connect
            if bool(project_manager.suspend):
                project_manager.suspend.Suspend.process_request(request, client)

        if type == 'resume':
            # Type RESUME means, it is a resume request of an existing suspended subscription in Connect
            if bool(project_manager.resume):
                project_manager.resume.Resume.process_request(request, client)

    # Check if the Usage usecase is included in this project
    if bool(project_manager.report_usage):
        # If the product contains items of type Pay-as-you-go, then the usage of such items needs to be submitted in Connect
        # Refer https://connect.cloudblue.com/community/modules/usage_module/ for more details about Usage in Connect

        # Check if the product has Pay-as-you-go (PAYG) items and capability
        # If yes, introduce the logic to set up frequency to report usage
        # This usage can be submitted as per the desired frequency
        # Here, for example, the processor reports usage at the last day of the month
        todays_date = datetime.today().date()
        last_day_of_month = monthrange(todays_date.year, todays_date.month)[1]
        if todays_date == last_day_of_month:
            # This will file a usage for a particular Provider, Product, Marketplace, Currency, Timezone and Period
            usage_file = project_manager.report_usage.Usage.create_usage_file(Globals.PRODUCTS[0], client)
            # The Usage file is an excel file which contains consumption details about the usage of PAYG items
            usage_excel = project_manager.report_usage.Usage.write_usage_file(Globals.PRODUCTS[0], client)
            # Upload this usage file in Connect that reports the consumption
            project_manager.report_usage.Usage.upload_usage(usage_file, client)
            # Submit the usage for this period and this product subscriptions to the Provider
            project_manager.report_usage.Usage.submit_usage(usage_file, client)




