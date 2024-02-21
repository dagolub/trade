from trade.services.interface import ExchangeInterface
from trade.services.binance_core.client import binance_exchange_rate  # type: ignore
from trade.core.config import settings
import requests

#
class Binance:
    async def get_exchange_info(self, from_coin, to_coin, amount=1.0, side="buy"):
        # url = "https://www.binance.com/bapi/margin/v1/private/new-otc/get-quote"
        # r = {"fromCoin": from_coin, "requestAmount": 1, "requestCoin": from_coin, "toCoin": to_coin,
        #            "walletType": "FUNDING"}
        # cookies = {'bnc-location': 'PL'}
        # cookies.setdefault('bnc-uuid', '783be6e2-a407-484a5-b281-eed94e2f4a67')
        # cookies.setdefault('__BNC__', '{"ca36767bf6718bd21eb24e018cc190d7":{"date":1694326332756,"value":"1694326332549ywM2fRHk0d445zz6PtU"}}')
        # headers = {'clienttype': 'web'}
        # headers.setdefault('bnc-uuid', '783be6e2-a407-484a5-b281-eed94e2f4a67')
        # headers.setdefault('x-ui-request-trace', '891af5d6-357d-40ba-88df-181de8004ac0')
        # headers.setdefault('x-trace-id', '891af5d6-357d-40ba-88df-181de8004ac0')
        # headers.setdefault('Host', 'www.binance.com')
        # respone = requests.post(url, data=r, cookies=cookies, headers=headers)
        rate = await binance_exchange_rate(f"{from_coin}{to_coin}")
        if rate is None:
            return -1, "", "", ""
        return rate, "", "", ""

    # okx = OKX_Client(
    #     settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE
    # )
    # data = okx.get_fee(currency)
    # for coin in data.get("data"):
    #     if coin.get("ccy") == currency:
    #         return coin.get("maxFee")
#     def buy_coins(self, in_currency, out_currency, amount):
#         raise NotImplementedError
#
#     def send_coins(self, from_address, to_address, amount):
#         raise NotImplementedError
#
#     def get_deposit_info(self, coin, address):
#         raise NotImplementedError
#
#     def get_pairs(self):
#         raise NotImplementedError
#
#     def get_pair(self, from_coin: str, to_coin: str):
#         raise NotImplementedError
#
#     def get_fee(self, coin):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         data = client.get_trade_fee()
#         for symbol in data:
#             if symbol.get("symbol") == f"{coin}{coin}":
#                 pass
#
#     def get_all_coins(self):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         return client.get_margin_all_assets()
#
#     async def get_coins(self, coin):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         tickers = client.get_all_tickers()
#         result = []
#         for ticker in tickers:
#             if ticker.get("symbol").endswith(coin):
#                 result.append(ticker)
#         return result
#
#     def exchange(self, from_coin, to_coin):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         client.universal_transfer()
#
#     def get_exchange_pairs(self):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         return client.get_orderbook_tickers()
#
#     def get_tickers(self):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         return client.get_all_tickers()
#
#     def get_ticker_price(self, from_coin, to_coin):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         return client.get_ticker(symbol=f"{from_coin}{to_coin}")
#

#
#     def create_order(self, symbol, quantity, price, side="BUY"):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         return client.create_order(
#             symbol=symbol,
#             side=side,
#             type="MARKET",
#             quantity=quantity,
#         )
#
#     def get_account(self):
#         client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
#         return client.get_account()
#
#     def estimate_quota(self, from_ccy, to_ccy, amount):
#         raise NotImplementedError
#
#     def get_orders(self, symbol):
#         raise NotImplementedError
