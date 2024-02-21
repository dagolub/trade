from dataclasses import dataclass
from trade.services.exchanger import Exchanger
from trade.services.interface import ExchangeInterface


@dataclass
class Operation:
    local_exchanger: ExchangeInterface
    foreign_exchanger: ExchangeInterface
    exchanger: Exchanger = Exchanger()

    local_from_currency: str = ""
    local_to_currency: str = ""
    local_from_amount: int = 0

    foreign_from_currency: str = ""
    foreign_to_currency: str = ""
    foreign_from_amount: int = 0

    def exchange(self, in_currency, out_currency, amount, exchanger):
        self.local_exchanger = Exchanger.get(exchanger)
        self.local_exchanger.buy_coins(in_currency, out_currency, amount)

    def send_to_another_exchanger(
        self, coin, chain, currency, from_exchanger, to_exchanger
    ):
        self.exchanger.send_to_another_exchanger(
            coin, chain, currency, from_exchanger, to_exchanger
        )

    async def initialize(self, db, binance, coin_name, amount):
        ...
        # obj_in = OperationCreate(**jsonable_encoder(data))
        # crud.operation.create(db, obj_in=obj_in)

    def local_exchange(self, in_currency, out_currency, amount, exchanger):
        self.exchange(in_currency, out_currency, amount, exchanger)

    def foreign_exchange(self, in_currency, out_currency, amount, exchanger):
        self.exchange(in_currency, out_currency, amount, exchanger)

    def send_back(self, coin, chain, currency, from_exchanger, to_exchanger):
        self.send_to_another_exchanger(
            coin, chain, currency, from_exchanger, to_exchanger
        )
