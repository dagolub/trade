import requests
from datetime import datetime
from app.services.okx_core.lib.Broker_api import BrokerAPI
from app.services.okx_core.lib.Convert_api import ConvertAPI
from app.services.okx_core.lib.Funding_api import FundingAPI as Funding
from app.services.okx_core.lib.Market_api import MarketAPI
from app.services.okx_core.lib.Public_api import PublicAPI
from app.services.okx_core.lib.Account_api import AccountAPI
from app.services.okx_core.lib.Trade_api import TradeAPI


def get_ip():
    response = requests.get("https://ipinfo.io/json", verify=True)

    if response.status_code != 200:
        raise ValueError(
            "Status:" + str(response.status_code) + "Problem with the request. Exiting."
        )

    return response.json().get("ip")


# def is_okx(db, wallet_address, sub_account=None):
#     address = wallet.get_by_address(db, wallet_address)
#     if address.customer.data.get("flags").get("okx_api"):
#         okx = OKX(
#             main_api_key=settings.OKX_API_KEY,
#             main_secret_key=settings.OKX_SECRET_KEY,
#             main_passphrase=settings.OKX_PASSPHRASE,
#             sub_account=sub_account if sub_account else address.customer.name,
#         )
#         return okx
#     return None


class OKX:
    main_api_key = ""
    main_secret_key = ""
    main_passphrase = ""

    def __init__(self, main_api_key, main_secret_key, main_passphrase):
        self.main_api_key = main_api_key
        self.main_secret_key = main_secret_key
        self.main_passphrase = main_passphrase

    def create_sub_account(self, sub_account):
        broker = BrokerAPI(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return broker.create_subaccount(sub_account, sub_account + "Label")

    def get_account(self, sub_account, ccy):
        chain = self.get_currency_chain("USDT", "trx")
        account = BrokerAPI(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return account.subaccount_deposit_address(sub_account, ccy, chain, 1, 6)

    def get_account_balance(self, ccy=None, api_key=None, secret_key=None, passphrase=None):
        if api_key:
            api_key = api_key
        else:
            api_key = self.main_api_key

        if secret_key:
            secret_key = secret_key
        else:
            secret_key = self.main_secret_key

        if passphrase:
            passphrase = passphrase
        else:
            passphrase = self.main_passphrase

        funding = Funding(api_key, secret_key, passphrase, flag="0")
        return funding.get_balances(ccy)

    def get_sub_account_api_key(self, sub_account, api_key):
        broker = BrokerAPI(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return broker.nd_select_apikey(sub_account, api_key)

    def create_sub_account_api_key(self, sub_account, sub_account_label, passphrase):
        ip = "165.22.19.20,2a03:b0c0:3:d0::197d:20015"
        broker = BrokerAPI(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return broker.nd_create_apikey(sub_account, sub_account_label, passphrase, ip, "withdraw")

    def transfer_money_to_main_account(self,
                                       ccy=None,
                                       amt=None,
                                       sub_account=None,
                                       from_account=None,
                                       to_account=None,
                                       type_transfer=None):

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
        funding = Funding(self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0")
        if sub_account:
            return funding.funds_transfer(ccy, amt, from_account, to_account, subAcct=sub_account, type=type_transfer)
        else:
            return funding.funds_transfer(ccy, amt, from_account, to_account, type=type_transfer)

    def make_withdrawal(self, currency=None, amount=None, address=None, chain=None,):
        try:
            funding = Funding(
                self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
            )

            withdrawals = funding.coin_withdraw(
                ccy=currency,
                amt=float(amount)-1,
                dest=4,
                toAddr=address,
                fee=1,
                chain="USDT-TRC20",
            )
            if len(withdrawals.get("data")) > 0:
                return withdrawals.get("data")[0]

            raise ValueError("Empty transaction")

        except Exception as e:
            raise ValueError("Failed to withdraw" + e.args[0])

    def get_withdrawal_history(self, ccy: str, wdId: str):
        funding = Funding(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return funding.get_withdrawal_history(ccy, wdId)

    def get_deposit_info(self, currency: str, chain: str, wallet_address: str) -> dict:
        return None

        trans = []
        if deposits.get("data"):
            address = crud_address.get_by_address(
                db=self.db, wallet_address=wallet_address
            )
            received = 0
            for tr in deposits.get("data"):
                if tr["to"] == wallet_address:
                    amount = self.fractional_to_integer(tr.get("amt"), currency, )
                    received += int(amount)
                    trans.append(
                        {
                            "txid": tr["txId"],
                            "date": str(tr["ts"]).replace("000", ""),
                            "amount": amount,
                            "status": "accepted",
                            "aml": {"riskscore": 0, "flags": None},
                        }
                    )

            data = {
                "address": address.address,
                "caller_id": address.caller_id,
                "since": str(datetime.timestamp(datetime.now())).split(".")[0],
                "received": received,
                "currency": self.populate_currency(currency.upper(), chain),
                "transactions": trans,
            }

            return data

        return None

    def check_limits(self, currency: str):
        funding = Funding(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        limits = funding.get_currency()

        for limit in limits.get("data"):
            if limit.get("ccy") == currency:
                return limit.get("minWd")

        return None

    async def send(self, data):
        return None
        # currency = currency_coin_and_chain(data.get('coin'))
        currency_chain = self.get_currency_chain(currency.coin, currency.network)
        limit = float(self.check_limits(currency.coin))
        balance = float(
            self.get_balance_of_main_account(currency.coin)
            .get("data")[0]
            .get("availBal")
        )

        if not self.get_balance_of_main_account(currency.coin).get("data"):
            raise ValueError("Insufficient main balance")

        for output in data.get("outputs"):
            amount = self.integer_to_fractional(output.get("amount"), currency.coin)
            if amount < limit:
                raise ValueError(
                    f"Some Withdrawal amount [{amount}] is lower than the lower limit[{limit}]."
                )

            if amount > balance:
                raise ValueError(
                    f"Some Withdrawal amount [{amount}] is more than the balance[{balance}]."
                )

            withdrawal = self.make_withdrawal(
                currency=currency.coin,
                chain=currency_chain,
                amount=amount,
                address=output.get("address"),
            )

            tx = self.get_withdrawal_history(
                currency=currency.coin, wd_id=withdrawal.get("wdId")
            )

            txid = tx.get("txId") if tx.get("txId") else withdrawal.get("wdId")
            data = {
                "txid": txid,
                "currency": self.populate_currency(currency.coin, currency.network),
            }

            data.setdefault(
                "amounts",
                [
                    {
                        "address": tx.get("to"),
                        "amount": self.fractional_to_integer(tx.get("amt"), currency.coin, ),
                    }
                ],
            )

            data.setdefault(
                "fee", self.fractional_to_integer(tx.get("fee"), currency.coin, )
            )

            return data

    def get_tickers(self):
        convert = MarketAPI(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return convert.get_tickers("SPOT")

    def get_ticker(self, symbol):
        convert = MarketAPI(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return convert.get_ticker(symbol)

    def create_order(self, symbol, quantity, price, side="sell"):
        cl_ord_id = "order" + str(datetime.now().timestamp()).replace(".", "")
        trade = TradeAPI(
            self.main_api_key, self.main_secret_key, self.main_passphrase, flag="0"
        )
        return trade.place_order(
            instId=symbol,
            tdMode="cash",
            side=side,
            ordType="limit",
            sz=quantity,
            clOrdId=cl_ord_id,
            px=price,
        )

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

    def fractional_to_integer(self, amount: str, currency: str) -> int:
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
    def get_currency_fee(currency: str, chain: str):
        if currency.lower() == "ltc":
            return 0.001
        if currency.lower() == "bch":
            return 0.00064
        if currency.lower() == "btc":
            return 0.0002
        if currency.lower() == "waves":
            return 0.0016
        if currency.lower() == "etc":
            return 0.008
        if currency.lower() == "eth":
            return 0.0006144
        if currency.lower() == "usdt":
            if chain.lower() == "usdt-erc20" or chain.lower() == "eth":
                return 3.7778016
            elif chain.lower() == "usdt-trc20" or chain.lower() == "trx":
                return 0.8

    @staticmethod
    def populate_currency(currency: str, chain: str):
        if currency.lower() == "ltc":
            return {"id": "ltc", "symbol": "LTC", "coin": "LTC", "decimals": 8}
        if currency.lower() == "bch":
            return {"id": "bch", "symbol": "BCH", "coin": "BCH", "decimals": 8}
        if currency.lower() == "waves":
            return {"id": "waves", "symbol": "WAVES", "coin": "WAVES", "decimals": 8}
        if currency.lower() == "btc":
            return {"id": "btc", "symbol": "BTC", "coin": "BTC", "decimals": 8}
        if currency.lower() == "etc":
            return {"id": "etc", "symbol": "ETC", "coin": "ETC", "decimals": 18}
        if currency.lower() == "eth":
            return {"id": "eth", "symbol": "ETH", "coin": "ETH", "decimals": 18}
        if currency.lower() == "usdt":
            if chain.lower() == "eth":
                return {"id": "usdteth", "symbol": "ETH", "coin": "USDT", "decimals": 6}
            elif chain.lower() == "trx":
                return {"id": "usdttrx", "symbol": "TRX", "coin": "USDT", "decimals": 6}

    @staticmethod
    def get_currency_chain(currency: str, chain: str):
        if currency.lower() == "ltc":
            return "LTC-Litecoin"
        if currency.lower() == "bch":
            return "BCH-BitcoinCash"
        if currency.lower() == "waves":
            return "WAVES-WAVES"
        if currency.lower() == "btc":
            return "BTC-Bitcoin"
        if currency.lower() == "usdt":
            if chain.lower() == "eth":
                return "USDT-ERC20"
            elif chain.lower() == "trx":
                return "USDT-TRC20"
        if currency.lower() == "etc":
            return "ETC-Ethereum Classic"
        if currency.lower() == "eth":
            return "ETH-ERC20"
