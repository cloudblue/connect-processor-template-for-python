from typing import Any
from openpyxl import Workbook
from datetime import datetime
from calendar import monthrange
import os
import ntpath
from connect_processor.app.utils.utils import Utils
from cnct import ConnectClient
from cnct import R


class Usage:
    def __init__(self, client: ConnectClient):
        self.client = client

    # This method loads the contracts and subscriptions to create and fill the usage file
    def process_usage(self):
        usage_data = Usage._get_usage_records()

        # Customize with Vendor API response
        if len(usage_data['subscriptions']) == 0:
            # no data to report
            return

        contracts = self._get_contracts()
        counter = 0
        # Retrieve the subscriptions for each contract
        for contract in contracts:
            query = R()

            # In preview all the subscription belongs to contract CRD-00000-00000-00000
            # use the next line for TEST purposes:
            # query &= R().contract.id.oneof(['CRD-00000-00000-00000'])
            query &= R().contract.id.oneof([contract['id']])
            query &= R().id.oneof([self._get_subscription_filter(usage_data)])

            subscriptions = self.client.collection("assets").filter(query)
            subscriptions.order_by('product.id')
            product_id = None
            record_data = []
            # Finds the subscriptions with usage data for each contract, create the Usage for each different product
            for subscription in subscriptions:
                counter = counter + 1
                if product_id is None:
                    product_id = subscription['product']['id']
                    self._validate_ppu_schema(product_id)
                if product_id != subscription['product']['id']:
                    self._create_usage(contract, product_id, record_data)
                    product_id = subscription['product']['id']
                    self._validate_ppu_schema(product_id)
                    record_data.clear()
                else:
                    # Using subscription usage data, fills the records collection
                    record_data.append(Usage._get_usage_data(subscription, usage_data))
            if product_id is not None:
                self._create_usage(contract, product_id, record_data)

        # Customize with Vendor API response
        if counter != len(usage_data['subscriptions']):
            # Check if all the subscriptions have been reported in the files.
            raise ValueError()

    @staticmethod
    def _get_subscription_filter(usage_data):
        # Customize with Vendor API response. From now assuming we have only one record to report
        return usage_data['subscriptions'][0]['id']

    def _get_contracts(self):
        # Loads the distribution contracts to find the subscriptions with data to build the reports
        query = R()
        query &= R().type.oneof(['distribution'])
        query &= R().status.oneof(['active'])
        contracts = self.client.collection("contracts").filter(query)
        return contracts

    @staticmethod
    def _get_usage_data(subscription, usage_data):
        # type: (Any, [Any]) -> UsageData
        # Retrieves th
        subs_usage_data = Utils.get_item_by_id(usage_data['subscriptions'], subscription['id'])
        usage_data_object = UsageData()
        usage_data_object.record_description = subscription['product']['name'] + " Period: " + subs_usage_data[
            'start_date'] + "-" + subs_usage_data['end_date']
        usage_data_object.item_mpn = subs_usage_data['mpn']
        usage_data_object.quantity = subs_usage_data['quantity']
        usage_data_object.start_time_utc = subs_usage_data['start_date']
        usage_data_object.end_time_utc = subs_usage_data['end_date']
        usage_data_object.asset_recon_id = subs_usage_data['id']
        return usage_data_object

    def _validate_ppu_schema(self, product_id):
        # type: (str) -> None
        # Retrieves the ppu schema to check if is QT, assumed for this template. If different raises NotImplementedError
        schema = self.client.collection('products')[product_id].get()['capabilities']['ppu']['schema']
        # using the schema Vendor can check if has to report Price, Quantity...
        if schema != "QT":
            raise NotImplementedError()

    # Loads the usage data from Vendor system calling Vendor API.
    @staticmethod
    def _get_usage_records():
        # Customize this to call vendor System and load the usage to report for each subscription.
        # It is need to retrieve the asset.id or the fulfillment parameter configured to indentify the subscription.
        # Also choose the reporting Schema, for this processor QT to report quantity.
        # For this sample the "id" is the asset.id.
        usage_data = {
            "subscriptions": [
                {
                    "id": "AS-####-####-####",
                    "mpn": "#####",  # The PAYG connect item MPN
                    "quantity": 10,  # This sample uses the QT model, use amount for PR
                    "start_date": '2021-02-01 00:00:00',  # Period reported. Format "%Y-%m-%d %H:%M:%S"
                    "end_date": '2021-02-28 00:00:00'
                }
            ]
        }
        return usage_data

    def _create_usage(self, contract, product_id, record_data):
        # type: (Any, str,  [UsageData]) -> None
        # Add a usage file for a Contract and product
        usage_file_id = self._create_usage_file(contract, product_id)
        # The Usage file has records with the consumption details about the usage of PAYG items
        usage_excel_path = Usage.UsageFileExcelCreator().create_usage_excel(record_data)
        # Upload this usage file in Connect that reports the consumption
        self._upload_usage(usage_file_id, usage_excel_path)
        # Submit the usage for this period and this product subscriptions to the Provider
        self._submit_usage(usage_file_id)

    def _create_usage_file(self, contract, product_id):
        # type: (Any, str) -> str
        # Creates a Usage report in Connect for a particular Contract and Product, in the month before the current.
        # Returns the usage file ID: UF-yyyy-mm-####-####
        contract_id = contract['id']
        currency = self.client.collection('marketplaces')[contract['marketplace']['id']].get()['currency']
        date_to = datetime(datetime.today().year, month=datetime.today().month - 1,
                           day=monthrange(datetime.today().year, datetime.today().month - 1)[1])
        date_from = datetime(datetime.today().year, month=datetime.today().month - 1, day=1)
        name = date_from.strftime("%d-%m-%Y") + " - " + date_to.strftime("%d-%m-%Y")
        # Customize to assign the external file id as your need.
        external_file_id = contract_id + " " + product_id + " " + datetime.today().strftime("%B")

        payload = {
            "name": name,
            "description": "Usage " + datetime.today().strftime("%B"),  # Can be changed
            "period": {
                "from": date_from.strftime("%Y-%m-%d"),
                "to": date_to.strftime("%Y-%m-%d")
            },
            "currency": currency,
            "product": {
                "id": product_id
            },
            "contract": {
                "id": contract_id
            },
            "external_id": external_file_id
        }
        file = self.client.ns('usage').files.create(payload=payload)
        return file['id']

    def _upload_usage(self, usage_file_id, usage_file_path):
        # type: (str, str) -> None
        # Uploads the Usage Excel file to Connect usage file
        file_data = open(usage_file_path, 'rb').read()
        file_name = ntpath.basename(usage_file_path)

        payload = {
            "usage_file": (file_name, file_data)
        }
        self.client.ns('usage').files[usage_file_id].action('upload').post(files=payload)

    def _submit_usage(self, usage_file_id):
        # type: (str) -> None
        # Submits the Usage report. This report will then be available to the Provider.
        self.client.ns('usage').files[usage_file_id].action('submit').post()

    class UsageFileExcelCreator:

        def create_usage_excel(self, record_data):
            # type: ([UsageData]) -> str
            # Creates the Excel .xlsx File and loads the records returning the file path
            excel_records = Usage.UsageFileExcelCreator._load_records(record_data)
            workbook = self._create_usage_records_sheet(records=excel_records)

            # Saves the file in the .config folder
            config_file = Utils.get_config_file()
            usage_path = config_file['rootPathUsage']
            if not os.path.exists(usage_path):
                os.mkdir(usage_path)
            path = usage_path + "/usage_file" + datetime.today().strftime("%Y%m%d%H%M%S") + ".xlsx"
            workbook.save(path)
            return path

        @staticmethod
        def _create_usage_records_sheet(records):
            # type: (List[ExcelUsageRecord]) -> Workbook
            # Creates the Excel WorkBook and completes the usage_records sheet
            book = Workbook()
            sheet = book.active
            sheet.title = 'usage_records'
            sheet['A1'] = 'record_id'
            sheet['B1'] = 'record_note'
            sheet['C1'] = 'item_search_criteria'
            sheet['D1'] = 'item_search_value'
            sheet['E1'] = 'amount'
            sheet['F1'] = 'quantity'
            sheet['G1'] = 'start_time_utc'
            sheet['H1'] = 'end_time_utc'
            sheet['I1'] = 'asset_search_criteria'
            sheet['J1'] = 'asset_search_value'
            sheet['K1'] = 'item_name'
            sheet['L1'] = 'item_mpn'
            sheet['M1'] = 'item_precision'
            sheet['N1'] = 'category_id'
            sheet['O1'] = 'asset_recon_id'
            sheet['P1'] = 'tier'
            for index, record in enumerate(records):
                row = str(index + 2)
                sheet['A' + row] = record.usage_record_id
                sheet['B' + row] = record.usage_record_note
                sheet['C' + row] = record.item_search_criteria
                sheet['D' + row] = record.item_search_value
                sheet['E' + row] = record.amount
                sheet['F' + row] = record.quantity
                sheet['G' + row] = record.start_time_utc
                sheet['H' + row] = record.end_time_utc
                sheet['I' + row] = record.asset_search_criteria
                sheet['J' + row] = record.asset_search_value
                sheet['K' + row] = record.item_name
                sheet['L' + row] = record.item_npm
                sheet['M' + row] = record.item_precision
                sheet['N' + row] = record.category_id
                sheet['O' + row] = record.asset_recon_id
                sheet['P' + row] = record.tier
            return book

        @staticmethod
        def _load_records(record_data):
            # type: (List[UsageData]) -> List[ExcelUsageRecord]
            # Returns the Excel rows to fill the File with the records data.
            usages = []
            for record in record_data:
                excel_record = ExcelUsageRecord()
                excel_record.usage_record_id = datetime.today().strftime("%Y%m%d%H%M%S")  # ToDo check criteria
                excel_record.usage_record_note = record.record_description
                excel_record.item_search_criteria = 'item.mpn'
                excel_record.item_search_value = record.item_mpn
                excel_record.quantity = record.quantity
                excel_record.amount = record.amount
                excel_record.start_time_utc = record.start_time_utc
                excel_record.end_time_utc = record.end_time_utc
                excel_record.asset_search_criteria = 'asset.id'  # could be 'parameter.[name of the parameter]]'
                # How to find the asset on Connect.  Typical use case is to use a parameter
                # provided by vendor, in this case use the parameter name, "subscription_id".  Additionally, asset.id
                # can be used in case you want to use Connect identifiers.
                excel_record.asset_search_value = record.asset_recon_id
                usages.append(excel_record)
            return usages


# Class to fill the Excel usage file.
class ExcelUsageRecord:
    usage_record_id = None  # type: str
    """ (str) Usage record id. """

    usage_record_note = None  # type: str
    """ (str) Usage record note. """

    item_search_criteria = None  # type: str
    """ (str) Item search criteria. """

    item_search_value = None  # type: str
    """ (str) Item search value. """

    amount = None  # type: float
    """ (float) Amount. """

    quantity = None  # type: int
    """ (int) Quantity. """

    start_time_utc = None  # type: str
    """ (str) Start Time in UTC. """

    end_time_utc = None  # type: str
    """ (str) End Time in UTC. """

    asset_search_criteria = None  # type: str
    """ (str) Asset search criteria. """

    asset_search_value = None  # type: str
    """ (str) Asset search value. """

    item_name = None  # type: str
    """ (str) Item name. """

    item_npm = None  # type: str
    """ (str) Item npm. """

    item_unit = None  # type: str
    """ (str) Item unit. """

    item_precision = None  # type: str
    """ (str) Item precision. """

    category_id = None  # type: str
    """ (str) Category Id. """

    asset_recon_id = None  # type: str
    """ (str) Asset recon Id. """

    tier = None  # type: str
    """ (str) Tier. """


# Class to retrieve the vendor usage data to fill the rows in the usage files (ExcelUsageRecord class)
class UsageData:
    record_description = None  # type: str
    """ (str) Usage record Description """
    # item MPN on Vendor portal
    item_mpn = None  # type: str
    """ (str) Usage record item MPN """
    # Quantity to report
    quantity = 1  # type: decimal
    """ (decimal) Usage record quantity """
    # Amount, price to report
    amount = 1  # type: decimal
    """ (decimal) Usage record amount """
    start_time_utc = None  # type: datetime
    """ (datetime) Date from """
    end_time_utc = None  # type: datetime
    """ (datetime) Date to """
    asset_recon_id = None  # type: str
    """ (str) Usage record asset or subscription fulfillment parameter id """
