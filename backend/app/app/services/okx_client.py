from abc import ABC

from app.services.interface import ExchangeInterface
from app.services.okx_core.client import OKX as OKX_Client
from app.core.config import settings


class OKX(ExchangeInterface, ABC):
    def get_address(self, sub_account, currency):
        try:
            okx = OKX_Client(
                settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
            )
        except ValueError:
            raise ValueError("OKX not available")
        sub_account_name = okx.create_sub_account(sub_account)
        account = okx.get_account(sub_account_name["data"][0]["subAcct"], currency)
        return account["data"][0]["addr"]

    def get_account_balance(self, ccy, api_key=None, secret_key=None, passphrase=None):
        try:
            okx = OKX_Client(
                settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
            )
        except:
            raise ValueError("OKX not accessible")
        return okx.get_account_balance(ccy, api_key, secret_key, passphrase)

    def get_sub_account_api_key(self, sub_account, api_key):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_sub_account_api_key(sub_account, api_key)

    def create_sub_account_api_key(self, sub_account, sub_account_label, passphrase):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.create_sub_account_api_key(sub_account, sub_account_label, passphrase)

    def transfer_money_to_main_account(self, ccy, amt, sub_account=None, from_account=None, to_account=None, type_transfer=None):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.transfer_money_to_main_account(ccy, amt, sub_account, from_account, to_account, type_transfer)

    def make_withdrawal(self, currency=None, amount=None, address=None):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.make_withdrawal(currency, amount, address)

    def frac_to_int(self, amount: str, currency: str) -> int:
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.fractional_to_integer(amount, currency)

    def int_to_frac(self, amount: str, currency: str) -> int:
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.integer_to_fractional(amount, currency)
