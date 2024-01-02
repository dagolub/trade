from app.services.okx.Broker_api import BrokerAPI
from app.services.okx.Funding_api import FundingAPI
from app.services.okx.subAccount_api import SubAccountAPI
from app.services.okx.Convert_api import ConvertAPI
from app.core.config import settings
import string
import random
from decimal import Decimal


def generate_random_small(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class OKX:
    funding = ""
    broker = ""

    def __init__(self):
        self.funding = FundingAPI(flag="0")
        self.broker = BrokerAPI(flag="0")

    def get_address(self, sub_account, currency, chain):
        chain = self.get_currency_chain(currency, chain)
        if not chain:
            ValueError("Wrong chain")
        try:
            self.broker.create_subaccount(sub_account, sub_account + "Label")
            account = self.broker.subaccount_deposit_address(
                sub_account, currency, chain, 1, 6
            )

            if len(account.get("data")) == 0:
                return "Cant create address"
            return account["data"][0]["addr"]
        except ValueError as e:
            raise ValueError("Can not create sub account " + sub_account + e.args[0])

    @staticmethod
    def get_deposit_history(ccy=None, api_key=None, secret=None, passphrase=None):
        funding = FundingAPI(
            flag="0", api_key=api_key, secret=secret, passphrase=passphrase
        )
        return funding.get_deposit_history(ccy)

    @staticmethod
    def get_sub_account_balance(sub_account, currency=None):
        account = SubAccountAPI(flag="0")
        if currency is None:
            currency = ""
        return account.asset_balances(subAcct=sub_account, ccy=currency)

    def create_sub_account_api_key(self, sub_account):
        ip = "178.128.196.184,165.22.19.20,104.248.131.103"

        sub_account_label = sub_account + generate_random_small(6)
        return self.broker.nd_create_apikey(
            sub_account, sub_account_label, settings.OKX_PASSPHRASE, ip, "withdraw"
        )

    def get_sub_account_api_keys(self, sub_account):
        return self.broker.nd_select_apikey(subAcct=sub_account)

    def delete_api_key(self, sub_account, api_key):
        return self.broker.nd_delete_apikey(subAcct=sub_account, apiKey=api_key)

    def get_currency_fee(self, _currency, chain):
        chain = self.get_currency_chain(_currency.lower(), chain)
        currencies = self.funding.get_currency()
        for currency in currencies["data"]:
            if currency["ccy"] == _currency.upper() and currency["chain"] == chain:
                return currency["minFee"]

    def transfer_money_to_main_account(
        self,
        ccy,
        amt,
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

        if sub_account:
            return self.funding.funds_transfer(
                ccy,
                amt,
                from_account,
                to_account,
                subAcct=sub_account,
                type=type_transfer,
            )
        else:
            return self.funding.funds_transfer(
                ccy, amt, from_account, to_account, type=type_transfer
            )

    def make_withdrawal(
        self, amount=None, address=None, currency=None, chain=None, fee=None
    ):
        try:
            withdrawals = self.funding.coin_withdraw(
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
            raise ValueError("Failed to withdraw" + str(e.args[0]))

    def get_withdrawal_history(self, ccy, wdId):
        return self.funding.get_withdrawal_history(ccy, wdId=wdId)

    def estimate_quota(self, from_ccy, to_ccy, amount, side="buy"):
        convert = ConvertAPI(flag="0")

        result = convert.estimate_quote(
            baseCcy=from_ccy,
            quoteCcy=to_ccy,
            side=side,
            rfqSz=amount,
            rfqSzCcy=from_ccy,
        )

        if (
            result["code"] == "58009"
            or result["code"] == "52914"  # noqa
            or result["code"] == "52915"  # noqa
        ):
            return False

        return result.get("data")[0]

    def convert_trade(self, from_ccy, to_ccy, amount, quota_id, side="buy"):
        convert = ConvertAPI(flag="0")

        result = convert.convert_trade(
            baseCcy=from_ccy,
            quoteCcy=to_ccy,
            side=side,
            sz=amount,
            szCcy=from_ccy,
            quoteId=quota_id,
        )

        return result

    def get_currencies(self):
        return self.funding.get_currency()

    @staticmethod
    def integer_to_fractional(amount: int, currency: str) -> float:
        currency = currency.lower()
        if currency in ("ltc", "btc"):
            f = Decimal(str(amount)) * Decimal("0.00000001")
            return float(f)
        if currency in ("usdt", "usdc"):
            f = Decimal(str(amount)) * Decimal("0.000001")
            return float(f)
        if currency in ("eth", "matic", "xrp", "solana", "trx", "ton"):
            f = Decimal(str(amount)) * Decimal("0.000000000000000001")
            return float(f)

    @staticmethod
    def fractional_to_integer(amount: float, currency: str) -> int:  # type: ignore
        currency = currency.lower()
        if currency in ("ltc", "btc"):
            _amount = Decimal(str(amount)) * 100000000
            return int(_amount)
        if currency in ("usdt", "usdc"):
            _amount = Decimal(str(amount)) * 1000000
            return int(_amount)
        if currency in ("eth", "matic", "xrp", "solana", "trx", "ton"):
            _amount = Decimal(str(amount)) * 1000000000000000000
            return int(_amount)

    @staticmethod
    def get_currency_chain(currency: str, chain: str):
        currency = currency.lower()
        chain = chain.lower()
        if currency == "ltc":
            return "LTC-Litecoin"
        if currency == "btc":
            return "BTC-Bitcoin"
        if currency == "usdt":
            if chain in ("eth", "erc20", "erc"):
                return "USDT-ERC20"
            elif chain in ("trx", "trc20", "trc"):
                return "USDT-TRC20"
            elif chain == "plg":
                return "USDT-Polygon"
        if currency == "eth":
            return "ETH-ERC20"
        if currency == "usdc":
            if chain in ("eth", "erc20"):
                return "USDC-ERC20"
            elif chain in ("trx", "trc20"):
                return "USDC-TRC20"
            elif chain == "plg":
                return "USDC-Polygon"
        if currency == "xrp":
            if chain == "ripple":
                return "XRP-Ripplse"
        if currency == "matic":
            if chain in ("erc", "erc20", "eth"):
                return "MATIC-ERC20"
        if currency == "matic":
            if chain in ("polygon"):
                return "MATIC-Polygon"
        if currency == "sol":
            if chain in ("solana"):
                return "SOL-Solana"
        if currency == "trx":
            if chain in ("trx", "trc20"):
                return "TRX-TRC20"
        if currency == "ton":
            if chain in ("ton"):
                return "TON-TON"
