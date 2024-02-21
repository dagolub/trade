# from trade.services.binance_client import Binance  # noqa
from trade.services.okx_client import OKX  # noqa
# from trade.services.mexc_client import MECX  # noqa
from trade.services.interface import ExchangeInterface
from dataclasses import dataclass


@dataclass
class Exchanger:
    @staticmethod
    def get(exchanger) -> ExchangeInterface:
        return eval(f"{exchanger}()")

    def send_to_another_exchanger(
        self, coin, chain, amount, from_exchanger, to_exchanger
    ):
        pass
