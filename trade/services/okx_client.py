from abc import ABC

from trade.services.interface import ExchangeInterface
from trade.services.okx_core.client import OKX as OKX_Client
from trade.core.config import settings


class OKX(ExchangeInterface, ABC):
    def buy_coins(self, in_currency, out_currency, amount):
        raise NotImplementedError

    def send_coins(self, from_address, to_address, amount):
        raise NotImplementedError

    def get_deposit_info(self, coin, address):
        raise NotImplementedError

    def get_coins(self, coin):
        raise NotImplementedError

    def get_all_coins(self):
        raise NotImplementedError

    def get_pairs(self, from_ccy, to_ccy, amount):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.estimate_quota(from_ccy, to_ccy, amount)

    def exchange(self, from_coin, to_coin):
        raise NotImplementedError

    def get_exchange_pairs(self):
        raise NotImplementedError

    def get_tickers(self):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_tickers()

    def get_ticker_price(self, from_coin, to_coin):
        raise NotImplementedError

    def get_exchange_info(self, from_coin, to_coin, side="buy", amount=1.0):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        # print(f"2. {from_coin} {to_coin} {amount} {side}")
        data, type = okx.estimate_quota(to_ccy=to_coin, from_ccy=from_coin, amount=amount, side=side)
        if not data:
            return -1, None, None, None
        if data.get("baseCcy") == from_coin and data.get("quoteCcy") == to_coin:
            return data.get("baseSz"), type, data.get("quoteId"), data
        return data.get("cnvtPx"), type, data.get("quoteId"), data

    def get_fee(self, currency):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        data = okx.get_fee(currency)
        for coin in data.get("data"):
            if coin.get("ccy") == currency:
                return coin.get("maxFee")

    def get_account(self):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_account()

    def covert_trade(self, from_ccy, to_ccy, amount, quota_id):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.convert_trade(from_ccy, to_ccy, amount, quota_id)

    def estimate_quota(self, from_ccy, to_ccy, amount):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.estimate_quota(from_ccy, to_ccy, amount)

    def create_order(self, symbol, quantity, price, side="sell"):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.create_order(symbol, quantity, price, side)

    def get_orders(self):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_orders()

    def get_ticker(self, symbol):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_ticker(symbol)

    def get_pair(self, from_coin: str, to_coin: str):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_pair(from_coin, to_coin)

    def funds_transfer(self, from_coin, from_balance, to_balance, amount):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.funds_transfer(from_coin, from_balance, to_balance, amount)

    def get_trading_balance(self, symbol):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.get_trading_balance(symbol)

    def get_account_balance(self, ccy, api_key=None, secret_key=None, passphrase=None):
        try:
            okx = OKX_Client(
                settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
            )
        except:
            raise ValueError("OKX not accessible")
        return okx.get_account_balance(ccy, api_key, secret_key, passphrase)

    def convert(self, from_ccy, to_ccy, amount, quoteId, side="buy"):
        try:
            okx = OKX_Client(
                settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
            )
        except:
            raise ValueError("OKX not accessible")
        print(f"  2. Convert from {from_ccy} to {to_ccy} {amount}")
        return okx.convert_trade(from_ccy=from_ccy, to_ccy=to_ccy, amount=amount, quota_id=quoteId, side=side)

    def transfer_money_to_main_account(
        self,
        ccy,
        amt,
        sub_account=None,
        from_account=None,
        to_account=None,
        type_transfer=None,
    ):
        okx = OKX_Client(
            settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
        )
        return okx.transfer_money_to_main_account(
            ccy, amt, sub_account, from_account, to_account, type_transfer
        )

if __name__ == "__main__":
    okx = OKX_Client(
        settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
    )
    # print(f"2. {from_coin} {to_coin} {amount} {side}")
    data = okx.estimate_quota(from_ccy="USDT", to_ccy="GOAL", amount=20, side="buy")

    print(data)