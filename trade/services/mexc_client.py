from abc import ABC

from trade.services.interface import ExchangeInterface
from .mexc_core.spot.v2.mexc_spot_v2 import get_symbols, get_ticker


class MECX(ExchangeInterface, ABC):
    def __init__(self):
        pass

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

    def get_pairs(self):
        result = []
        symbols = get_symbols()
        for symbol in symbols.get("data"):
            coin = get_ticker(symbol.get("symbol")).get("data")[0]
            from_coin, to_coin = coin.get("symbol").split("_")
            result.append(
                {
                    "from_coin": from_coin,
                    "to_coin": to_coin,
                    "bid": coin.get("bid"),
                    "ask": coin.get("ask"),
                    "rate": coin.get("change_rate"),
                }
            )
        return result

    def exchange(self, from_coin, to_coin):
        raise NotImplementedError

    def get_exchange_pairs(self):
        raise NotImplementedError

    def get_tickers(self):
        raise NotImplementedError

    def get_ticker_price(self, from_coin, to_coin):
        raise NotImplementedError

    def get_exchange_info(self, from_coin, to_coin):
        raise NotImplementedError

    def get_fee(self, currency):
        raise NotImplementedError

    def get_account(self):
        raise NotImplementedError

    def covert_trade(self, from_ccy, to_ccy, amount, quota_id):
        raise NotImplementedError

    def estimate_quota(self, from_ccy, to_ccy, amount):
        raise NotImplementedError

    def create_order(self, symbol, quantity, price, side="sell"):
        raise NotImplementedError

    def get_orders(self):
        raise NotImplementedError

    def get_ticker(self, symbol):
        raise NotImplementedError

    def get_pair(self, from_coin: str, to_coin: str):
        raise NotImplementedError

    def funds_transfer(self, from_coin, from_balance, to_balance, amount):
        raise NotImplementedError

    def get_trading_balance(self, symbol):
        raise NotImplementedError
