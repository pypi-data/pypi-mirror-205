import requests
import json
from dhosting_api.base_email import BaseAdapter
from requests.auth import HTTPBasicAuth
from . import exceptions


class DhostingAdapter(BaseAdapter):
    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.url = "https://api.dhosting.pl"
        self.headers = self._set_headers()
        self.auth = self._auth(username, pwd)

    def make_request(self, endpoint, body, method):
        url = self.url + endpoint
        payload = json.dumps(body)
        response = requests.request(method, url, headers=self.headers, data=payload, auth=self.auth)
        if response.status_code == 200:
            try:
                return self._prepare_response(response)
            except KeyError:
                return response
        else:
            self._handle_error(response, endpoint)

    def _prepare_response(self, response):
        response_dict = json.loads(response.text)['Data']
        return response_dict

    def _auth(self, username, pwd):
        return HTTPBasicAuth(username, pwd)

    def _set_headers(self):
        return {'Accept': 'application/json', 'Accept-Language': 'pl'}

    def get_url(self):
        return self.url

    def _handle_error(self, response, endpoint):
        error_number = response.json()['ErrorCode']

        if endpoint == '/email/createMailbox':
            if error_number == 120450:
                raise exceptions.BadEmailSyntax
            elif error_number == 120451:
                raise exceptions.BadPhoneNumberParameter
            elif error_number == 120452:
                raise exceptions.InvalidPassword
            elif error_number == 120457:
                raise exceptions.QuotaLimitExceeded
            elif error_number == 120458:
                raise exceptions.BadSendSMSParameter
            elif error_number == 120460:
                raise exceptions.ServiceLimitsExceeded
            elif error_number == 120470:
                raise exceptions.EmailAccountExists
            else:
                self._handle_error(response, endpoint)

        if endpoint == '/email/getMailboxList':
            if error_number == 120458:
                raise exceptions.BadDomainName
            else:
                self._generic_exception(response)

        if endpoint == '/emailAlias/createAlias':
            if error_number == 130420:
                raise exceptions.AliasAddedToSameEmail
            if error_number == 130440:
                raise exceptions.AliasAlreadyExist

        if error_number == 120450:
            raise exceptions.MailboxDoesntExist
        elif error_number == 120460:
            raise exceptions.OperationError
        else:
            self._generic_exception(response)

    def _generic_exception(self, response):
        raise Exception(response.text)
