import unittest
import os
from cnct import ConnectClient
from connect_processor.app.report_usage import Usage, UsageData
from unittest.mock import patch, MagicMock
from test_util import TestUtils

config_file = TestUtils.get_config_file()
# apiEndpoint is the API End-point of Connect
connect_api_url = config_file['connectApiEndpoint']
# apiKey is the API key for authorization created in Integrations menu of Connect
connect_key = config_file['connectApiKey']
# products are the list of IDs of the products which needs to be processed by this Processor
client = ConnectClient(api_key=connect_key, endpoint=connect_api_url)


class TestUsage(unittest.TestCase):

    @patch('connect_processor.app.report_usage.Usage._get_usage_records',
           MagicMock(return_value={
               "subscriptions": [
                   {
                       "id": "AS-8055-3268-5577",
                       "mpn": "MPN-A",
                       "quantity": 10,
                       "start_date": '2021-02-01 00:00:00',
                       "end_date": '2021-02-28 00:00:00'
                   }
               ]
           }))
    def test_report_usage_pass(self):
        with self.assertRaises(ValueError):
            Usage(client).process_usage()

    def test_create_excel_file(self):
        usage_data = UsageData()
        usage_data.record_description = 'Test product Period: TEST'
        usage_data.item_mpn = "MPN-A"
        usage_data.quantity = 20
        usage_data.start_time_utc = '2021-02-01 00:00:00'
        usage_data.end_time_utc = '2021-02-28 00:00:00'
        usage_data.asset_recon_id = 'AS-8055-3268-5577'
        record_data = [usage_data]
        path = Usage.UsageFileExcelCreator().create_usage_excel(record_data)
        self.assertTrue(os.path.exists(path))
        os.remove(path)
