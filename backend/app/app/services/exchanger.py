from dataclasses import dataclass

from app.services.interface import ExchangeInterface
from app.services.okx_client import OKX  # noqa


@dataclass
class Exchanger:
    @staticmethod
    def get(exchanger) -> ExchangeInterface:
        return eval(f"{exchanger}()")
