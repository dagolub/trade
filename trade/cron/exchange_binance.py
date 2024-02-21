from trade.services.exchanger import Exchanger
from trade.db.session import database as db
import anyio
from trade.crud.crud_exchange_binance import exchange_binance as crud
from trade.schemas.exchange_binance import ExchangeBinanceCreate
from datetime import datetime, timezone


async def main():
    binance = Exchanger.get("Binance")

    exchange_pairs = binance.get_exchange_pairs()

    all_symbols = binance.get_all_coins()

    total = 0
    for a in exchange_pairs:
        total += 1
        from_coin, to_coin = get_from_to_symbol(all_symbols, a.get("symbol"))
        if from_coin and to_coin:
            data = {
                "customer_id": 1,
                "to_coin": to_coin,
                "from_coin": from_coin,
                "price": a.get("bidPrice"),
                "added": str(datetime.now(timezone.utc)),
            }

            await crud.create(db, obj_in=[ExchangeBinanceCreate(**data)])
        
        else:
            pass
    print("Total: ", total)

def get_from_to_symbol(all_symbols, symbol):
    symbols = [a.get("assetName") for a in all_symbols]
    from_coin = to_coin = None
    for s in symbols:
        if s in symbol:
            if symbol.endswith(s):
                from_coin = symbol.replace(s, "")
                to_coin = s
            else:
                from_coin = s
                to_coin = symbol.replace(s, "")

    return from_coin, to_coin


if __name__ == "__main__":
    anyio.run(main)
