from trade.db.session import database as db
from trade.services.exchanger import Exchanger
from trade.schemas.pair import PairCreate
from fastapi.encoders import jsonable_encoder
import anyio
from trade.crud.crud_pair import pair as crud


async def main():
    amount = 1000
    binance = Exchanger.get("Binance")
    okx = Exchanger.get("OKX")

    result = []
    # data = binance.get_exchange_pairs()
    #
    # tickers_binance = binance.get_tickers()
    # for ticker in tickers_binance:
    #     if len(ticker.get('symbol')) == 6:
    #         from_coin, to_coin = ticker.get('symbol')[0:3], ticker.get('symbol')[3:6]
    #         tickers_okx = okx.get_tickers(to_coin, from_coin)
    #         if len(tickers_okx.get('data')) > 0:
    #             a = 1000/float(ticker.get('price'))/float(tickers_okx.get('data')[0].get('cnvtPx'))
    #             result.append(a)
    result = []
    all_coins = binance.get_all_coins()
    for a in all_coins:
        coin = a.get("assetName")
        coins = await binance.get_coins(coin)

        for c in coins:
            to_ccy = c.get("symbol").replace(coin, "")
            pair = okx.get_pairs(coin, to_ccy, amount)
            if len(pair.get("data")) > 0:
                to = pair.get("data")[0].get("cnvtPx")
                a = 1000 * float(c.get("price")) * float(to)
                if a > 955:
                    result.append(
                        {
                            "to": pair.get("data")[0].get("baseCcy"),
                            "from": pair.get("data")[0].get("quoteCcy"),
                            "profit": a,
                            "from_price": float(c.get("price")),
                            "to_price": float(pair.get("data")[0].get("cnvtPx")),
                        }
                    )

    for r in result:
        if r.get("to") == "USDT":
            continue
        db_obj = crud.get_by_start_send(db, r.get("to"), r.get("from"))
        send_coin_amount = 1000 * r.get("from_price")
        receive_coin_amount = send_coin_amount - get_fee(r.get("to"))
        final_coin_amount = receive_coin_amount * r.get("to_price")
        profit = final_coin_amount - 1000 - get_backward_fee(r.get("from"))
        data = {
            "from_exchanger": "Binance",
            "start_coin": r.get("from"),
            "send_coin": r.get("to"),
            "receive_coin": r.get("to"),
            "final_coin": r.get("from"),
            "to_exchanger": "OKX",
            "start_coin_amount": 1000,
            "send_coin_amount": send_coin_amount,
            "send_fee": get_fee(r.get("to")),
            "receive_coin_amount": receive_coin_amount,
            "final_coin_amount": final_coin_amount,
            "backward_fee": get_backward_fee(r.get("from")),
            "profit": profit,
        }
        obj_in = PairCreate(**jsonable_encoder(data))
        if db_obj:
            crud.update(db, db_obj=db_obj, obj_in=obj_in)
        else:
            crud.create(db, obj_in=obj_in)


def get_fee(currency: str):
    if currency.upper() == "ETH":
        return 0.000768
    if currency.upper() == "DOGE":
        return 4


def get_backward_fee(currency: str):
    if currency.upper() == "UNI":
        return 0.480334144
    if currency.upper() == "SHIB":
        return 322209.855630448
    if currency.upper() == "TRX":
        return 0.8
    if currency.upper() == "XRP":
        return 0.2


if __name__ == "__main__":
    anyio.run(main)
