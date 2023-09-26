from app.services.okx_core.client import OKX as OKX_Client
from app.services.okx_core.lib.Broker_api import BrokerAPI


class OKX:
    okx = ""

    def __init__(self):
        self.okx = OKX_Client()

    def get_address(self, sub_account, currency, chain):
        chain = self.get_currency_chain(currency, chain)

        account = BrokerAPI(flag="0")
        account = account.subaccount_deposit_address(sub_account, currency, chain, 1, 6)

        if len(account.get("data")) == 0:
            return "Cant create address"
        return account["data"][0]["addr"]

    def get_account_balance(self, ccy, api_key=None, secret_key=None, passphrase=None):
        return self.okx.get_account_balance(ccy, api_key, secret_key, passphrase)

    def get_sub_account_api_key(self, sub_account, api_key):
        return self.okx.get_sub_account_api_key(sub_account, api_key)

    def delete_api_key(self, sub_account, api_key):
        return self.okx.delete_api_key(sub_account=sub_account, api_key=api_key)

    def create_sub_account_api_key(self, sub_account, sub_account_label, passphrase):
        return self.okx.create_sub_account_api_key(
            sub_account, sub_account_label, passphrase
        )

    def get_sub_account_api_keys(self, sub_account):
        return self.okx.get_sub_account_api_keys(sub_account)

    def get_deposit_history(self, ccy=None, api_key=None, secret=None, passphrase=None):
        self.okx = OKX_Client()
        return self.okx.get_deposit_history(ccy)

    def get_currency_fee(self, currency, chain):
        return self.okx.get_currency_fee(_currency=currency, chain=chain)

    def transfer_money_to_main_account(
        self,
        ccy,
        amt,
        sub_account=None,
        from_account=None,
        to_account=None,
        type_transfer=None,
    ):
        return self.okx.transfer_money_to_main_account(
            ccy, amt, sub_account, from_account, to_account, type_transfer
        )

    def make_withdrawal(
        self, amount=None, address=None, currency=None, chain=None, fee=None
    ):
        return self.okx.make_withdrawal(
            amount=amount, address=address, currency=currency, chain=chain, fee=fee
        )

    def get_withdrawal_history(self, ccy, wdId):
        return self.okx.get_withdrawal_history(ccy, wdId)

    def frac_to_int(self, amount: str, currency: str) -> int:
        return self.okx.fractional_to_integer(amount, currency)

    def int_to_frac(self, amount: str, currency: str) -> int:
        return self.okx.integer_to_fractional(amount, currency)

    @staticmethod
    def integer_to_fractional(amount: str, currency: str):
        if currency.lower() in ("ltc", "bch", "btc", "waves"):
            _amount = int(amount) * 0.00000001
            return float(f"{_amount:.100f}")
        if currency.lower() == "usdt":
            _amount = int(amount) * 0.000001
            return float(f"{_amount:.100f}")
        if currency.lower() in ("eth", "etc"):
            _amount = int(amount) * 0.000000000000000001
            return float(f"{_amount:.100f}")

    @staticmethod
    def fractional_to_integer(amount: str, currency: str) -> int:  # type: ignore
        if currency.lower() in ("ltc", "bch", "btc", "waves"):
            _amount = float(amount) * 100000000
            return int(f"{_amount:.0f}")
        if currency.lower() == "usdt":
            _amount = float(amount) * 1000000
            return int(f"{_amount:.0f}")
        if currency.lower() in ("etc", "eth"):
            _amount = float(amount) * 1000000000000000000
            return int(f"{_amount:.0f}")

    @staticmethod
    def get_currency_chain(currency: str, chain: str):
        currency = currency.lower()
        chain = chain.lower()
        if currency == "ltc":
            return "LTC-Litecoin"
        if currency == "bch":
            return "BCH-BitcoinCash"
        if currency == "btc":
            return "BTC-Bitcoin"
        if currency == "usdt":
            if chain == "eth":
                return "USDT-ERC20"
            elif chain == "trx":
                return "USDT-TRC20"
            elif chain == "plg":
                return "USDT-Polygon"
        if currency == "etc":
            return "ETC-Ethereum Classic"
        if currency == "eth":
            return "ETH-ERC20"
