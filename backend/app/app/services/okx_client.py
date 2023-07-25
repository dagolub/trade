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

    def get_account_balance(self, api_key, secret_key, passphrase, ccy):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_account_balance(api_key, secret_key, passphrase, ccy)

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
