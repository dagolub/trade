from trade.services.exchanger import Exchanger
from trade.db.session import database as db
import anyio
from trade.crud.crud_exchange_mecx import exchange_mecx as crud
from trade.schemas.exchange_mecx import ExchangeMECXCreate
from datetime import datetime


async def main():
    mecx = Exchanger.get("MECX")

    tickers = mecx.get_pairs()
    total = 0
    for a in tickers:
        data1 = {
            "customer_id": 1,
            "to_coin": a.get("from_coin"),
            "from_coin": a.get("to_coin"),
            "price": float(a.get("ask")),
            "rate": float(a.get("rate")),
            "added": datetime.utcnow(),
        }

        data2 = {
            "customer_id": 1,
            "to_coin": a.get("to_coin"),
            "from_coin": a.get("from_coin"),
            "price": float(a.get("bid")),
            "rate": float(a.get("rate")),
            "added": datetime.utcnow(),
        }

        obj_in = [ExchangeMECXCreate(**data1), ExchangeMECXCreate(**data2)]
        await crud.create(db, obj_in=obj_in)

        total += 2
    print("New tickers: ", total)


if __name__ == "__main__":
    anyio.run(main)
