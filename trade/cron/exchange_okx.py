from trade.services.exchanger import Exchanger
from trade.db.session import database as db
import anyio
from trade.crud.crud_exchange_okx import exchange_okx as crud
from trade.schemas.exchange_okx import ExchangeOKXCreate
from datetime import datetime, timezone


async def main():
    okx = Exchanger.get("OKX")

    tickers = okx.get_tickers()
    total = 0
    for a in tickers.get("data"):
        from_coin, to_coin = a.get("instId").split("-")
        if from_coin and to_coin:
            data = {
                "customer_id": 1,
                "to_coin": to_coin,
                "from_coin": from_coin,
                "price": float(a.get("bidPx")),
                "added": str(datetime.now(timezone.utc)),
            }

            await crud.create(db, obj_in=[ExchangeOKXCreate(**data)])
            total += 1
    print("New tickers: ", total)


if __name__ == "__main__":
    anyio.run(main)
