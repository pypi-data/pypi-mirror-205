import string
import secrets
from .adapter import DhostingAdapter
from dhosting_api.base_email import BaseEmailProvider
from django.conf import settings


USER = getattr(settings, 'DHOSTING').get('DHOSTING_USERNAME', None)
PASSWORD = getattr(settings, 'DHOSTING').get('DHOSTING_PASSWORD', None)


class DhostingProvider(BaseEmailProvider):
    def __init__(self) -> None:
        super().__init__()

    adapter = DhostingAdapter(USER, PASSWORD)

    def get_mailbox_list(self, domain):
        endpoint = "/email/getMailboxList"
        body = {"Domain": domain}
        method = 'POST'
        return self.adapter.make_request(endpoint, body, method)['MailboxList']

    def create_mailbox(self, email, pwd, phone_number='', send_sms=False, quota=5.0, unlimited=False):
        endpoint = '/email/createMailbox'
        body = {
            "MailboxName": email,
            "Password": pwd,
            "PhoneNumber": phone_number,
            "SendSms": send_sms,
            "Quota": quota,
            "mailboxQuotaUnlimited": unlimited,
        }
        method = 'POST'
        self.adapter.make_request(endpoint, body, method)
        return self.get_mailbox(email)

    def get_mailbox_information(self, email):
        endpoint = "/email/getMailboxInformation"
        body = {"MailboxName": email}
        method = "POST"
        return self.adapter.make_request(endpoint, body, method)

    def change_mailbox_quota(self, email, limit):
        endpoint = "/email/changeMailboxQuota"
        if self.check_limit(limit):
            body = {"MailboxName": email, "Quota": limit}
            method = "PUT"
            return self.adapter.make_request(endpoint, body, method)

    def change_mailbox_status(self, email, status):
        endpoint = '/email/changeMailboxStatus'
        body = {"MailboxName": email, "NewStatus": status}
        method = "PUT"
        return self.adapter.make_request(endpoint, body, method)

    def delete_mailbox(self, email):
        endpoint = '/email/deleteMailbox'
        body = {"MailboxName": email}
        method = "DELETE"
        return self.adapter.make_request(endpoint, body, method)

    def create_alias(self, email, alias, description=''):
        endpoint = '/emailAlias/createAlias'
        body = {
            "AliasAddres": alias,
            "Description": description,
            "MailBoxes": [
                email,
            ],
        }
        method = 'POST'
        return self.adapter.make_request(endpoint, body, method)

    def delete_alias(self, alias):
        endpoint = '/emailAlias/deleteAlias'
        body = {"AliasName": alias}
        method = 'DELETE'
        return self.adapter.make_request(endpoint, body, method)

    def get_mailboxes(self, domain):
        mailboxes = []

        for email in self.get_mailbox_list(domain):
            mailboxes.append(Mailbox(email))

        return mailboxes

    def get_mailbox_quota(self, email):
        return self.get_mailbox_information(email)['quota']['limit_skrzynki_mb']

    def get_mailbox(self, email):
        return Mailbox(email)

    def generate_password(self, n):
        alphabet = string.ascii_letters + string.digits + '!@^&*()_+<>'
        pwd = ''
        for i in range(n):
            pwd += ''.join(secrets.choice(alphabet))
        return pwd

    def check_limit(self, limit):
        if limit < 10:
            return True
        elif limit == -1:
            return True
        else:
            return False


class Mailbox:
    provider = DhostingProvider()

    def __init__(self, email):
        self.email = email

    def get_mailbox_information(self):
        return self.provider.get_mailbox_information(self.email)

    def get_quota(self):
        return self.provider.get_mailbox_quota(self.email)

    def change_quota(self, quota):
        return self.provider.change_mailbox_quota(self.email, quota)

    def create_alias(self, alias):
        return self.provider.create_alias(self.email, alias)

    def delete_alias(self, alias):
        return self.provider.delete_alias(alias)

    def delete(self):
        return self.provider.delete_mailbox(self.email)

    def disable_account(self):
        return self.provider.change_mailbox_status(self.email, False)

    def enable_account(self):
        return self.provider.change_mailbox_status(self.email, True)

    def __str__(self):
        return self.email
