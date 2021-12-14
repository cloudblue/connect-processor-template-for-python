import requests
from requests import RequestException

from connect_ext.utils.message import Message


class APIClient(object):
    access_token = None
    authorization_header = None

    # API constructor.
    def __init__(self, api_url):
        self.type = ''
        # The Mock API hasn't an API KEY.
        self.api_url = api_url

    def authenticated(self):
        self.authorization_header = {'Content-Type': 'application/json'}

    def create_subscription(self, data):
        self.authenticated()
        url = self.api_url + '/tenant'

        r = requests.post(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r.json()

    def change_subscription(self, data, subscription_id):
        self.authenticated()

        url = self.api_url + "/tenant/" + subscription_id

        r = requests.put(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r.json()

    def cancel_subscription(self, data, subscription_id):
        self.authenticated()

        url = self.api_url + '/tenant/' + subscription_id

        r = requests.delete(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r

    def suspend_subscription(self, data, subscription_id):
        self.authenticated()

        url = self.api_url + '/tenant/' + subscription_id + '/disable'

        r = requests.put(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r

    def resume_subscription(self, data, subscription_id):
        self.authenticated()

        url = self.api_url + '/tenant/' + subscription_id + '/enable'

        r = requests.put(url=url, json=data, headers=self.authorization_header)
        self._check_and_pack_response(r)
        return r

    def _check_and_pack_response(self, r):
        # Review and use the different Error Codes from ISV API
        request_attrs = ('json', 'status_code', 'ok')

        for attr in request_attrs:
            if not hasattr(r, attr):
                raise RequestException(Message.RESPONSE_DOES_NOT_HAVE_ATTRIBUTE.format(attr, r.status_code))
            if int(r.status_code) >= 299 and int(r.status_code) != 400:
                raise RequestException(Message.RESPONSE_ERROR.format(r.status_code, r.text))
