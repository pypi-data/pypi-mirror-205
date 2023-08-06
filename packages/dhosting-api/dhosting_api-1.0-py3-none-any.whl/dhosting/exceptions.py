class EmailAccountExists(Exception):
    pass


class InvalidPassword(Exception):
    pass


class ServiceLimitsExceeded(Exception):
    pass


class BadEmailSyntax(Exception):
    pass


class BadSendSMSParameter(Exception):
    pass


class QuotaLimitExceeded(Exception):
    pass


class BadPhoneNumberParameter(Exception):
    pass


class MailboxDoesntExist(Exception):
    pass


class BadDomainName(Exception):
    pass


class OperationError(Exception):
    pass


class DisallowedMarks(Exception):
    pass


class AliasAlreadyExist(Exception):
    pass

