from connect_processor.app.utils.globals import Globals
from tempfile import NamedTemporaryFile
import os

class Usage():
    def create_usage_file(product_id, client):
        payload = {
            "name": "string",
            "description": "string",
            "note": "string",
            "period": {
                "from": "2021-02-27",
                "to": "2021-02-27"
            },
            "currency": "USD",
            "product": {
             "id": "PRD-714-131-720"
            },
            "contract": {
                "id": "CRD-00000-00000-00000"
            },
            "external_id": ""
            }
        file = client('usage').files
        # client.usage('files').create(payload=payload)
        file = client('usage').files.create(payload=payload)
        # client.usage.files('create').post(payload=payload)
        # client.usage('files').post(payload=payload)
        return file['id']

    def upload_usage(usage_file_id, client):
        usage_path = os.path.join(os.path.realpath(os.path.curdir),'app','usage_file.xlsx')

        bin_data = open(usage_path, 'rb').read()

        files = {'file': bin_data}

        result = client('usage').files[usage_file_id].upload.create(payload=files, )

        return result


    def submit_usage(usage_file_id, client):

        # client.usage[usage_file_id]('submit').post(payload=hex_data)
        result = client('usage').files[usage_file_id].submit.update()
        # client.requests[request_id]('approve').post(payload=payload1)
        return result

