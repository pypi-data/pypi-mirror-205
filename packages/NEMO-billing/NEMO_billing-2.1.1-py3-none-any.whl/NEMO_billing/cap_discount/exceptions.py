from NEMO.models import Account

from NEMO_billing.exceptions import BillingException


class MissingCAPAmountException(BillingException):
    def __init__(self, month, account: Account):
        msg = f"Could not find prior CAP records for {month.strftime('%B %Y')} for account: '{account.name}'. Please generate invoices for that month and try again."
        super().__init__(msg)


class NotLatestInvoiceException(BillingException):
    pass
