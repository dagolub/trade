import anyio
from trade.db.session import database as db
from sqlalchemy.sql import text  # type: ignore
from trade.services.exchanger import Exchanger


async def main():
    binance = Exchanger.get("Binance")

    pairs = db.execute(
        text("select from_coin, to_coin from exchange group by from_coin, to_coin")
    )

    result = {}
    last_prices = {}
    for pair in pairs:
        from_coin, to_coin = pair
        if to_coin == "USDT":
            average_sql = f"select avg(price) from exchange where from_coin='{from_coin}' and to_coin='{to_coin}'"
            avg = list(db.execute(text(average_sql)))[0][0]
            last_price_sql = (
                f"select price from exchange where from_coin='{from_coin}' and to_coin='{to_coin}'"
                f"order by added desc"
            )
            last_price = list(db.execute(text(last_price_sql)))[0][0]
            last_prices.setdefault(f"{from_coin}{to_coin}", last_price)
            if last_price > 0:
                result.setdefault(f"{from_coin}{to_coin}", round(avg / last_price, 2))

    sorted_result = {
        key: val
        for key, val in sorted(result.items(), key=lambda ele: ele[1], reverse=True)
    }
    pair, diff = list(sorted_result.items())[0]
    bid_price = last_prices[pair] * 1.001
    print(bid_price)
    account = binance.get_account()
    for balance in account.get("balances"):
        if balance.get("asset") == "YFII":
            print(balance)
    buy_quantity = round(50 / float(bid_price))  # noqa
    data = binance.create_order(symbol=pair, quantity=0.008, price=round(bid_price, 2))
    print(data)


if __name__ == "__main__":
    anyio.run(main)
