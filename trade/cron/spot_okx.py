import anyio
from trade.db.session import database as db
from sqlalchemy.sql import text  # type: ignore
from trade.services.exchanger import Exchanger
import math


async def main():  # noqa
    okx = Exchanger.get("OKX")

    pairs = db.execute(
        text("select from_coin, to_coin from exchange_okx group by from_coin, to_coin")
    )

    result = {}
    last_prices = {}
    for pair in pairs:
        from_coin, to_coin = pair
        if to_coin == "USDT":
            average_sql = f"select avg(price) from exchange_okx where from_coin='{from_coin}' and to_coin='{to_coin}' "
            avg = list(db.execute(text(average_sql)))[0][0]
            last_price_sql = (
                f"select price from exchange_okx where from_coin='{from_coin}' and to_coin='{to_coin}' "
                f"order by added desc offset 0 limit 1"
            )
            # f"order by added desc"
            # data = crud.exchange_okx.get_multi(db, ExchangeOKX.from_coin == from_coin, ExchangeOKX.to_coin == to_coin,
            #                                    order_by=ExchangeOKX.added, skip=0, limit=1)
            last_price_result = list(db.execute(text(last_price_sql)))
            if len(list(last_price_result)) == 0:
                continue
            try:
                last_price = list(last_price_result)[0][0]
                pass
            except Exception as e:
                print(e)
                continue
            last_prices.setdefault(f"{from_coin}-{to_coin}", last_price)
            if last_price > 0:
                result.setdefault(f"{from_coin}-{to_coin}", round(avg / last_price, 2))

    if result:
        orders = okx.get_orders()
        if len(orders.get("data")) > 0:
            print("Order exist")
            exit()

        trading_balance = okx.get_trading_balance("USDT")

        usdt_balance = 0
        for details in trading_balance.get("data"):
            for balance in details["details"]:
                if balance.get("ccy") == "USDT":
                    if math.floor(float(balance.get("availBal"))) > 1:
                        usdt_balance = math.floor(float(balance.get("availBal")))
                        okx.funds_transfer("USDT", usdt_balance, 18, 6)
                        print("Transfer balance to funding", usdt_balance)

        sorted_result = {
            key: val
            for key, val in sorted(result.items(), key=lambda ele: ele[1], reverse=True)
        }
        pair, diff = list(sorted_result.items())[0]
        from_coin, to_coin = pair.split("-")
        account = okx.get_account()
        available_usdt_balance = 0
        for balance in account.get("data"):
            if balance["ccy"] == "USDT":
                available_usdt_balance = float(balance["availBal"])

        print("Available funding balance")
        if available_usdt_balance > 1:
            estimate_quota = okx.estimate_quota(
                from_coin, to_coin, available_usdt_balance
            )
            quota_id = estimate_quota.get("data")[0].get("quoteId")
            okx.covert_trade(to_coin, from_coin, available_usdt_balance, quota_id)
            print("Convert funding balance")
            available_balance = 0
            account = okx.get_account()
            for balance in account.get("data"):
                if balance["ccy"] == from_coin:
                    available_balance = float(balance["availBal"])

            okx.funds_transfer(from_coin, available_balance, 6, 18)
            # ticker = okx.get_ticker(pair).get('data')[0].get('last')
            # ticker_price = float(ticker)*1.01
            trading_balance = okx.get_trading_balance(from_coin)
            ticker_price = float(estimate_quota.get("data")[0].get("cnvtPx")) * 1.0015
            balance_to_buy = 0
            for details in trading_balance.get("data"):
                for balance in details["details"]:
                    if balance.get("ccy") == from_coin:
                        balance_to_buy = balance.get("availBal")
            print("Trading balance", balance_to_buy)
            order = okx.create_order(
                f"{from_coin}-{to_coin}", balance_to_buy, ticker_price
            )
            print(order)


if __name__ == "__main__":
    anyio.run(main)
