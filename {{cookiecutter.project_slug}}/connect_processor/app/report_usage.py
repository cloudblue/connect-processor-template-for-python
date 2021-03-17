
import os

class Usage():
    # This is step 1, to create a Usage report in Connect for a particular Provider, Product, Marketplace, Currency, Timezone and Period
    # Customize this method to provide the above mentioned details in the payload
    # This method will create the Usage report entry in Connect and return the ID generated for the same
    def create_usage_file(product_id, client):
        # ToDo: replace the static data with the inf from Connect
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

        file = client('usage').files.create(payload=payload)

        return file['id']

    def write_usage_file(product_id, client):
        # TpDo:implementation pending
        usage_path = os.path.join(os.path.realpath(os.path.curdir), 'app', 'usage_file.xlsx')

    # This method will upload the Usage excel file to Connect

    def upload_usage(usage_file_id, client):
        # ToDo:change this file path with the file that will be written by this processor
        usage_path = os.path.join(os.path.realpath(os.path.curdir),'app','usage_file.xlsx')

        bin_data = open(usage_path, 'rb').read()

        files = {'file': bin_data}

        result = client('usage').files[usage_file_id].upload.create(payload=files, )

        return result

    # This is final step #3 to submit the Usage report. This report will then be available to the Provider.
    def submit_usage(usage_file_id, client):

        result = client('usage').files[usage_file_id].submit.update()

        return result

