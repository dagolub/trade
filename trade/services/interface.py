from abc import ABC, abstractmethod


class ExchangeInterface(ABC):
    @abstractmethod
    def buy_coins(self, in_currency, out_currency, amount):
        raise NotImplementedError

    @abstractmethod
    def send_coins(self, from_address, to_address, amount):
        raise NotImplementedError

    @abstractmethod
    def get_deposit_info(self, coin, address):
        raise NotImplementedError

    @abstractmethod
    def get_coins(self, coin):
        raise NotImplementedError

    @abstractmethod
    def get_fee(self, coin):
        raise NotImplementedError

    @abstractmethod
    def get_pairs(self):
        raise NotImplementedError

    @abstractmethod
    def get_pair(self, from_coin: str, to_coin: str):
        raise NotImplementedError

    def get_all_coins(self):
        raise NotImplementedError

    def exchange(self, from_coin, to_coin):
        raise NotImplementedError

    def get_exchange_pairs(self):
        raise NotImplementedError

    def get_tickers(self):
        raise NotImplementedError

    def get_ticker(self, symbol):
        raise NotImplementedError

    def get_ticker_price(self, from_coin, to_coin):
        raise NotImplementedError

    def get_exchange_info(self, from_coin, to_coin, side, amount):
        raise NotImplementedError

    def create_order(self, symbol, quantity, price, side="buy"):
        raise NotImplementedError

    def get_account(self):
        raise NotImplementedError

    def covert_trade(self, from_ccy, to_ccy, amount, quota_id):
        raise NotImplementedError

    def estimate_quota(self, from_ccy, to_ccy, amount):
        raise NotImplementedError

    def get_orders(self):
        raise NotImplementedError

    def create_order(self, symbol, quantity, price, side="sell"):
        raise NotImplementedError

    def funds_transfer(self, from_coin, from_balance, to_balance, amount):
        raise NotImplementedError

    def get_trading_balance(self, symbol):
        raise NotImplementedError

    def get_account_balance(self, ccy,  api_key=None, secret_key=None, passphrase=None):
        raise NotImplementedError

    def convert(self, from_ccy, to_ccy, amount, quoteId, side="buy"):
        raise NotImplementedError