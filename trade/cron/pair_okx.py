from trade.services.exchanger import Exchanger
import anyio
import json
import requests
import re
import timeout_decorator


async def main():
    stop = False
    coefficient = []
    # rate = await get_exchange_rate("LTC", "USDT")
    ccys = get_ccy()
    total = 0
    for i in ccys:
        stop = False
        if "USDT" != i:
            rate, type = get_exchange_rate("USDT", i)
            if rate > 0:
                print(f"Get exchange rate USDT -> {i} = {rate}")
                if rate:

                    for j in ccys:

                        if j != "USDT" and i != j and not stop:
                            print(f".", end="")

                            rate2, type2 = get_exchange_rate(i, j)

                            if rate2 > 0:
                                nn = 0
                                for n in ccys:
                                    print(f"*", end="")
                                    # nn = nn + 1
                                    # if nn == 3:
                                    #     break
                                    if n != "USDT" and n != j and not stop:
                                        rate3, type3 = get_exchange_rate(j, n)
                                        if rate3 > 0:
                                            rate4, type4 = get_exchange_rate(n, "USDT")
                                            if rate4 > 0:

                                                c = 1

                                                if type == "buy":
                                                    c = c / rate
                                                else:
                                                    c = c * rate

                                                if type2 == "buy":
                                                    c = c / rate2
                                                else:
                                                    c = c * rate2

                                                if type3 == "buy":
                                                    c = c / rate3
                                                else:
                                                    c = c * rate3

                                                if type4 == "buy":
                                                    c = c / rate4
                                                else:
                                                    c = c * rate4
                                                coefficient.append(c)
                                                print("")
                                                print("MAX = ", end="")
                                                max_coef = max(coefficient)
                                                print(max_coef, " - ", total)
                                                if max_coef > 1.2:
                                                    exit(1)
                                                total = total + 1
                                                if total == 1:
                                                    stop = True
                                                    total = 0
                                                # if c > 1.01 and c < 2:
                                                # if c > 0.99:
                                                print("")
                                                print(
                                                    f"-- USDT [{rate}-{type}] {i} [{rate2}-{type2}] {j} [{rate3}-{type3}] {n} [{rate4}-{type4}] USDT = {c}"
                                                )
    #


def get_exchange_rate(from_coin, to_coin):
    try:
        url = "https://www.okx.com/v2/asset/quick/exchange/quote"
        data_sell = {
            "baseCcy": f"{from_coin}",
            "quoteCcy": f"{to_coin}",
            "side": "sell",
            "rfqSz": "10",
            "rfqSzCcy": f"{from_coin}",
        }
        request_sell = re.sub("\s", "", json.dumps(data_sell))
        headers_sell = {
            "Host": "www.okx.com",
            "Content-Length": str(len(request_sell)),
        }
        response_sell = requests.post(url, json=data_sell, headers=headers_sell, timeout=1).json()
        data_buy = {
            "baseCcy": f"{to_coin}",
            "quoteCcy": f"{from_coin}",
            "side": "buy",
            "rfqSz": "10",
            "rfqSzCcy": f"{from_coin}",
        }
        request_buy = re.sub("\s", "", json.dumps(data_buy))
        headers_buy = {
            "Host": "www.okx.com",
            "Content-Length": str(len(request_buy)),
        }
        response_buy = requests.post(url, json=data_buy, headers=headers_buy, timeout=1).json()
        try:
            ask_sell = bid_sell = ask_buy = bid_buy = 0
            if "askPx" in response_sell["data"]:
                ask_sell = float(response_sell["data"]["askPx"])
            if "bidPx" in response_sell["data"]:
                bid_sell = float(response_sell["data"]["bidPx"])
            if "askPx" in response_buy["data"]:
                ask_buy = float(response_buy["data"]["askPx"])
            if "bidPx" in response_buy["data"]:
                bid_buy = float(response_buy["data"]["bidPx"])
            if ask_sell > 0:
                return ask_sell, "sell"
            if bid_sell > 0:
                return bid_sell, "sell"
            if ask_buy > 0:
                return ask_buy, "buy"
            if bid_buy > 0:
                return bid_buy, "buy"
            return 0, "none"
        except Exception as e:
            return 0, "none"
    except Exception as e:
        return 0, "none"


def get_ccy():
    url = "https://www.okx.com/v2/asset/quick/exchange/currencies"
    response = requests.get(url).json()["data"]
    ccys = []
    for i in response:
        ccys.append(i["ccy"])
    return ccys


anyio.run(main)
