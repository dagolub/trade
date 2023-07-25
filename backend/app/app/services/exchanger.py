from app.services.okx_client import OKX  # noqa
from app.services.interface import ExchangeInterface
from dataclasses import dataclass


@dataclass
class Exchanger:
    @staticmethod
    def get(exchanger) -> ExchangeInterface:
        return eval(f"{exchanger}()")
