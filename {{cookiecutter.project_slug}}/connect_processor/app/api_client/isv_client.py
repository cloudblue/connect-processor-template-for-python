import requests
from app.utils.message import Message
from connect.exceptions import SkipRequest
# from oauthlib.oauth2 import LegacyApplicationClient
# from requests_oauthlib import OAuth2Session

BODY_TAIL = "\n/// ********************"

class APIClient(object):
    access_token = None
    authorization_header = None

    # API constructor.
    def __init__(self, api_url, api_key):
        self.type = ''
        self.api_url = api_url
        self.api_key = api_key

    def authenticated(self):

            # This code can be used when token needs to be generated through an API
            # oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))
            # self.access_token = oauth.fetch_token(
            #     token_url=self.token_url, username=self.username, password=self.password,
            #     client_id=self.client_id, include_client_id=False, client_secret=self.client_secret
            # )

            # If just an API access key is required for authorization
            # self.access_token = base64.b64encode(self.api_key)
            # logger.info('Authenticated')

            # Provide Authorization info in header
            # self.authorization_header = {'Authorization': 'Basic ' + self.api_key['api_key']}
            self.authorization_header = {'Content-Type': 'application/json'}

    def create_subscription(self, data):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant'
        # Method: Post
        r = requests.post(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r.json()

    def change_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id
        # Method: Put
        r = requests.put(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r.json()

    def cancel_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id

        # Method: Delete
        r = requests.delete(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r


    def suspend_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id + '/disable'
        # Method: Delete
        r = requests.put(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r


    def resume_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id + '/enable'
        # Method: Delete
        r = requests.put(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r


    def _check_and_pack_response(self, r):
        request_attrs = ('json', 'status_code', 'ok')
        for attr in request_attrs:
            if not hasattr(r, attr):
                raise SkipRequest(Message.Shared.RESPONSE_DOES_NOT_HAVE_ATTRIBUTE.format(attr, r.status_code))
            if int(r.status_code) >= 299 and int(r.status_code) != 400:
                raise SkipRequest(Message.Shared.RESPONSE_ERROR.format(r.status_code, r.text))
