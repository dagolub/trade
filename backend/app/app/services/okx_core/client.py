import requests  # type: ignore
from app.services.okx_core.lib.Broker_api import BrokerAPI
from app.services.okx_core.lib.Funding_api import FundingAPI as Funding


def get_ip():
    response = requests.get("https://ipinfo.io/json", verify=True)

    if response.status_code != 200:
        raise ValueError(
            "Status:" + str(response.status_code) + "Problem with the request. Exiting."
        )

    return response.json().get("ip")


class OKX:
    def create_sub_account(self, sub_account):
        try:
            broker = BrokerAPI(flag="0")
            result = broker.create_subaccount(sub_account, sub_account + "Label")
            return result
        except ValueError as e:
            raise ValueError("Can not create sub account " + sub_account + e.args[0])

    def get_account(self, sub_account, ccy, chain):
        chain = self.get_currency_chain(ccy, chain)
        account = BrokerAPI(flag="0")
        return account.subaccount_deposit_address(sub_account, ccy, chain, 1, 6)

    def get_account_balance(
        self, ccy=None, api_key=None, secret_key=None, passphrase=None
    ):
        funding = Funding(flag="0")
        return funding.get_balances(ccy)

    def get_sub_account_api_key(self, sub_account, api_key):
        broker = BrokerAPI(flag="0")
        return broker.nd_select_apikey(sub_account, api_key)

    def create_sub_account_api_key(self, sub_account, sub_account_label, passphrase):
        ip = "178.128.196.184,165.22.19.20"
        broker = BrokerAPI(flag="0")

        result = broker.nd_create_apikey(
            sub_account, sub_account_label, passphrase, ip, "withdraw"
        )

        return result

    def get_sub_account_api_keys(self, sub_account):
        broker = BrokerAPI(flag="0")
        return broker.nd_select_apikey(subAcct=sub_account)

    def delete_api_key(self, sub_account, api_key):
        broker = BrokerAPI(flag="0")
        return broker.nd_delete_apikey(subAcct=sub_account, apiKey=api_key)

    def transfer_money_to_main_account(
        self,
        ccy=None,
        amt=None,
        sub_account=None,
        from_account=None,
        to_account=None,
        type_transfer=None,
    ):
        if from_account:
            from_account = from_account
        else:
            from_account = 6

        if to_account:
            to_account = to_account
        else:
            to_account = 18

        if type_transfer is not None:
            type_transfer = type_transfer
        else:
            type_transfer = 2
        funding = Funding(flag="0")
        if sub_account:
            return funding.funds_transfer(
                ccy,
                amt,
                from_account,
                to_account,
                subAcct=sub_account,
                type=type_transfer,
            )
        else:
            return funding.funds_transfer(
                ccy, amt, from_account, to_account, type=type_transfer
            )

    def make_withdrawal(
        self, currency=None, amount=None, address=None, chain=None, fee=None
    ):
        try:
            funding = Funding(flag="0")

            withdrawals = funding.coin_withdraw(
                ccy=currency.upper(),
                amt=float(amount) - float(fee),
                dest=4,
                toAddr=address,
                fee=fee,
                chain=chain,
            )
            if withdrawals["code"] == "58350":
                raise ValueError("Insufficient balance, try to " + str(amount))

            if len(withdrawals.get("data")) > 0:
                return withdrawals.get("data")[0]

            raise ValueError("Empty transaction")

        except Exception as e:
            raise ValueError("Failed to withdraw" + e.args[0])

    def get_withdrawal_history(self, ccy: str, wd_id: str):
        funding = Funding(flag="0")
        return funding.get_withdrawal_history(ccy, wdId=wd_id)

    @staticmethod
    def get_deposit_history(ccy=None):
        funding = Funding(flag="0")
        return funding.get_deposit_history(ccy)

    def get_currency_fee(self, _currency: str, chain: str):
        chain = self.get_currency_chain(_currency.lower(), chain)
        funding = Funding(flag="0")
        currencies = funding.get_currency()
        for currency in currencies["data"]:
            if currency["ccy"] == _currency.upper() and currency["chain"] == chain:
                return currency["minFee"]

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
