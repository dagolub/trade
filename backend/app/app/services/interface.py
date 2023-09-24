from abc import ABC, abstractmethod


class ExchangeInterface(ABC):
    def __init__(self):
        self.fractional_to_integer = None

    @abstractmethod
    def get_address(self, sub_account: str, currency: str, chain: str):
        raise NotImplementedError

    @abstractmethod
    def get_account_balance(
        self, api_key: str, secret_key: str, passphrase: str, ccy: str
    ):
        raise NotImplementedError

    def get_sub_account_api_key(self, sub_account, api_key):
        raise NotImplementedError

    def create_sub_account_api_key(self, sub_account, sub_account_label, passphrase):
        raise NotImplementedError

    def get_sub_account_api_keys(self, sub_account):
        raise NotImplementedError

    def delete_api_key(self, sub_account, api_key):
        raise NotImplementedError

    def transfer_money_to_main_account(
        self, ccy, amt, sub_account, from_account, to_account, type_transfer
    ):
        raise NotImplementedError

    def make_withdrawal(
        self, amount=None, address=None, currency=None, chain=None, fee=None
    ):
        raise NotImplementedError

    def get_withdrawal_history(self, ccy, wdId):
        raise NotImplementedError

    def get_deposit_history(self, ccy=None, api_key=None, secret=None, passphrase=None):
        raise NotImplementedError

    def get_currency_chain(self, currency, chain):
        raise NotImplementedError

    def get_currency_fee(self, _currency, chain):
        raise NotImplementedError

    @abstractmethod
    def frac_to_int(self, amount: str, currency: str):
        raise NotImplementedError

    @abstractmethod
    def int_to_frac(self, amount: str, currency: str):
        raise NotImplementedError
