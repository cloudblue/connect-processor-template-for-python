import requests
import json
import time
import base64
from app.class_models.credentials import Credentials
from app.utils.logger import logger, function_log
from app.utils.message import Message
from connect.exceptions import SkipRequest
# from oauthlib.oauth2 import LegacyApplicationClient
# from requests_oauthlib import OAuth2Session

BODY_TAIL = "\n/// ********************"

class APIClient(object):
    access_token = None
    authorization_header = None

    # API constructor.
    def __init__(self, credentials: Credentials):
        self.type = ''
        self.api_url = credentials.api_url
        self.api_key = credentials.api_key

    @function_log
    def authenticated(self):
            logger.info('>>> Authenticating <<<')

            # This code can be used when token needs to be generated through an API
            # oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id))
            # self.access_token = oauth.fetch_token(
            #     token_url=self.token_url, username=self.username, password=self.password,
            #     client_id=self.client_id, include_client_id=False, client_secret=self.client_secret
            # )

            # If just an API access key is required for authorization
            # self.access_token = base64.b64encode(self.api_key)
            logger.info('Authenticated')

            # Provide Authorization info in header
            # self.authorization_header = {'Authorization': 'Basic ' + self.api_key['api_key']}
            self.authorization_header = {'Content-Type': 'application/json'}

    @function_log
    def create_subscription(self, data):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant'

        logger.info('>>> Create account. <<<')
        logger.info(f"\n/// REQUEST ********************\nURL: {url}\nBODY: {json.dumps(data) + BODY_TAIL}")
        # Method: Post
        r = requests.post(url=url, json=data, headers=self.authorization_header)
        logger.info(f"\n/// RESPONSE ********************\nStatus >>> {r.status_code}\nHeaders >>> {r.headers}\nContent >>> {str(r.json())}\n/// ********************")
        self._check_and_pack_response(r)
        return r.json()

    @function_log
    def change_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id

        logger.info('>>> Change subscription. <<<')
        logger.info(f"\n/// REQUEST ********************\nURL: {url}\nBODY: {json.dumps(data) + BODY_TAIL}")
        # Method: Put
        r = requests.put(url=url, json=data, headers=self.authorization_header)
        logger.info(
            f"\n/// RESPONSE ********************\nStatus >>> {r.status_code}\nHeaders >>> {r.headers}\nContent >>> {str(r.json())}\n///********************")
        self._check_and_pack_response(r)
        return r.json()

    @function_log
    def cancel_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id

        logger.info('>>> Cancel subscription. <<<')
        logger.info(f"\n/// REQUEST ********************\nURL: {url}\nBODY: {json.dumps(data) + BODY_TAIL}")
        # Method: Delete
        r = requests.delete(url=url, json=data, headers=self.authorization_header)
        logger.info(
            f"\n/// RESPONSE ********************\nStatus >>> {r.status_code}\nHeaders >>> {r.headers}\nContent >>> {r.content}\n///********************")
        self._check_and_pack_response(r)
        # return r.json()
        return r

    @function_log
    def suspend_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id + '/disable'

        logger.info('>>> Suspend subscription. <<<')
        logger.info(f"\n/// REQUEST ********************\nURL: {url}\nBODY: {json.dumps(data) + BODY_TAIL}")
        # Method: Delete
        r = requests.put(url=url, json=data, headers=self.authorization_header)
        logger.info(
            f"\n/// RESPONSE ********************\nStatus >>> {r.status_code}\nHeaders >>> {r.headers}\nContent >>> {r.content}\n///********************")
        self._check_and_pack_response(r)
        # return r.json()
        return r

    @function_log
    def resume_subscription(self, data, tenant_id):
        # self.authenticated()

        # Customize the url as per the Vendor APIs
        url = self.api_url + '/tenant/' + tenant_id + '/enable'

        logger.info('>>> Resume subscription. <<<')
        logger.info(f"\n/// REQUEST ********************\nURL: {url}\nBODY: {json.dumps(data) + BODY_TAIL}")
        # Method: Delete
        r = requests.put(url=url, json=data, headers=self.authorization_header)
        logger.info(
            f"\n/// RESPONSE ********************\nStatus >>> {r.status_code}\nHeaders >>> {r.headers}\nContent >>> {r.content}\n///********************")
        self._check_and_pack_response(r)
        # return r.json()
        return r

    @function_log
    def _check_and_pack_response(self, r):
        request_attrs = ('json', 'status_code', 'ok')
        for attr in request_attrs:
            if not hasattr(r, attr):
                logger.error(Message.Shared.RESPONSE_DOES_NOT_HAVE_ATTRIBUTE.format(attr, r.status_code))
                raise SkipRequest(Message.Shared.RESPONSE_DOES_NOT_HAVE_ATTRIBUTE.format(attr, r.status_code))
            if int(r.status_code) >= 299 and int(r.status_code) != 400:
                logger.error(Message.Shared.RESPONSE_ERROR.format(r.status_code, r.text))
                raise SkipRequest(Message.Shared.RESPONSE_ERROR.format(r.status_code, r.text))
