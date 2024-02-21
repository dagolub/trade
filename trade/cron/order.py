import time

import anyio
from fastapi.encoders import jsonable_encoder
from trade import crud
from trade.db.session import database as db
from sqlalchemy.sql import text  # type: ignore
from trade.models.order import OrderStatus
from trade.schemas.order import OrderCreate, OrderUpdate
from trade.services.exchanger import Exchanger
from datetime import datetime, timezone


async def main():
    okx = Exchanger.get("OKX")

    volatility_sql = (
        "select from_coin, to_coin, price from volatility WHERE "
        "from_coin!='BUSD' and to_coin!='BUSD' and from_coin!='BNB' and to_coin!='BNB'"
        "order by price desc"
    )
    volatilises = list(db.execute(text(volatility_sql)))
    total_order = 0

    for v in volatilises:
        from_coin, to_coin, volatility = v
        not_okx_coin = [
            "MBL",
            "T",
            "TRIBE",
            "SFP",
            "BIFI",
            "LAZIO",
            "ONG",
            "TKO",
            "PORTO",
            "SANTOS",
            "POLYX",
            "JUV",
            "VXG",
            "Y",
            "MBL",
            "VGX",
            "TWT",
            "SCRT",
            "HIVE",
            "SCRT",
            "PLA",
            "GMX",
            "PLA",
            "AION",
            "XRPDOWM",
            "STPT",
            "QI",
            "CHESS",
            "DF",
            "ASR",
            "ATM",
            "ACM",
            "OOKI",
            "XVG",
            "BAR",
            "PSG",
            "MFT",
            "PUNDIX",
            "NEBl",
        ]
        if from_coin in not_okx_coin or to_coin in not_okx_coin:
            continue
        if to_coin != "USDT":
            continue

        avg_volatility_sql = (
            f"select avg(price) from exchange where "
            f"from_coin = '{from_coin}' and to_coin='{to_coin}'"
        )
        average_price = list(db.execute(text(avg_volatility_sql)))[0][0]
        binance = Exchanger.get("Binance")
        ticker = binance.get_ticker_price(from_coin, to_coin)
        exchange_pair = okx.get_exchange_info(to_coin, from_coin)
        time.sleep(1)
        if (
            float(ticker.get("askPrice")) < float(average_price) * 0.97
            and total_order < 10  # noqa
            and exchange_pair  # noqa
        ):
            exchange_info_sql = f"select price from exchange where from_coin = '{from_coin}' and to_coin='USDT'"
            if len(list(db.execute(text(exchange_info_sql)))) == 0:
                continue
            to_usdt_price = list(db.execute(text(exchange_info_sql)))[0][0]

            start_coin = 100 / to_usdt_price
            data = {
                "customer_id": 1,
                "from_coin": from_coin,
                "to_coin": to_coin,
                "buy_price": ticker.get("askPrice"),
                "status": OrderStatus.OPEN,
                "start_coin": start_coin,
                "added": str(datetime.now(timezone.utc)),
            }
            obj_in = OrderCreate(**jsonable_encoder(data))
            crud.order.create(db, obj_in=obj_in)
            total_order += 1

    orders_sql = "select id, from_coin, to_coin, buy_price, start_coin from \"order\" where status='open'"
    orders = list(db.execute(text(orders_sql)))
    for order in orders:
        order_id, from_coin, to_coin, buy_price, start_coin = order
        exchange_pair = okx.get_exchange_info(to_coin, from_coin)
        time.sleep(1)
        if exchange_pair:
            price = exchange_pair.get("cnvtPx")
            finish_coin = 100.8 * float(price)
            fee = okx.get_fee(from_coin)
            start_coin = finish_coin - float(fee)

            exchange_info_sql = f"select price from exchange where from_coin = '{from_coin}' and to_coin='USDT'"
            exchange_from_to_coin_to_usdt = list(db.execute(text(exchange_info_sql)))[
                0
            ][0]

            finish_coin_usdt = start_coin / float(exchange_from_to_coin_to_usdt)
            profit_usdt = finish_coin_usdt - 100

            greed_level = 0
            if profit_usdt > greed_level:
                data = {
                    "sell_price": price,
                    "start_coin": start_coin,
                    "finish_coin": finish_coin,
                    "profit": 0,
                    "profit_usd": profit_usdt,
                    "status": OrderStatus.CLOSED,
                    "updated": str(datetime.now(timezone.utc)),
                }
                db_obj = crud.order.get(db, order_id)
                obj_in = OrderUpdate(**jsonable_encoder(data))
                crud.order.update(db, db_obj=db_obj, obj_in=obj_in)


if __name__ == "__main__":
    anyio.run(main)
