import smtplib
import typer
import asyncio
from trade.db.session import database as db
from datetime import datetime
from trade import crud
from time import sleep
from trade.services.exchanger import Exchanger
import redis
from trade.core.config import settings
from trade.services.okx_client import OKX

coins = (
    "CAPO",
    "TRUE",
    "GOAL",
    "BTM",
    "BLOK",
    "INT",
    "TRX",
    "SUN",
    "KCASH",
    "LDN",
    "SD",
    "TAI",
    "ONT",
    "TURBO",
    "GMT",
    "NEO",
    "SNX",
    "TAKI",
    "RSS3",
    "IOTA",
    "JST",
    "VELODROME",
    "TUP",
    "SSV",
    "FAME",
    "WIN",
    "ACH",
    "NFT",
    "CGL",
    "MRST",
    "MXT",
    "VELO",
    "SHIB",
    "AZY",
    "ADA",
    "ELF",
    "GOG",
    "FSN",
    "RON",
    "QTUM",
    "LINK",
    "GAS",
    "JOE",
    "PSTAKE",
    "LAMB",
    "XMR",
    "CRV",
    "LPT",
    "CFG",
    "PEOPLE",
    "BSV",
    "CVX",
    "OKB",
    "WAVES",
    "BZZ",
    "FLM",
    "CFX",
    "AVAX",
    "CEL",
    "YFI",
    "MKR",
    "GRT",
    "YFII",
    "BAT",
    "BTT",
    "WNCG",
    "LING",
    "TOWN",
    "UTK",
    "LQTY",
    "ZEN",
    "AR",
    "ALPHA",
    "ETH",
    "HNT",
    "BAL",
    "DORA",
    "IOST",
    "1INCH",
    "WBTC",
    "BETH",
    "HC",
    "DOGE",
    "DAI",
    "USDC",
    "EC",
    "ILV",
    "MITH",
    "RAY",
    "SUSHI",
    "EURT",
    "DOT",
    "XCH",
    "XAUT",
    "BTC",
    "DGB",
    "AXS",
    "BNB",
    "PICKLE",
    "SPELL",
    "ATOM",
    "ZBC",
    "ZKS",
    "DASH",
    "MANA",
    "NYM",
    "OKT",
    "CORE",
    "TAMA",
    "WXT",
    "KAN",
    "RPL",
    "CQT",
    "BCD",
    "APM",
    "KONO",
    "XTZ",
    "KLAY",
    "DEP",
    "MATIC",
    "ANT",
    "COVER",
    "BCH",
    "CHZ",
    "FLOW",
    "MLN",
    "XRP",
    "AGLD",
    "BNT",
    "XLM",
    "EGT",
    "GARI",
    "TRA",
    "EM",
    "SAMO",
    "REN",
    "BONE",
    "CEEK",
    "RSR",
    "AAVE",
    "CELR",
    "FODL",
    "SAND",
    "KDA",
    "PNK",
    "RACA",
    "ALGO",
    "CRO",
    "MDT",
    "DCR",
    "GLMR",
    "ZRX",
    "EGLD",
    "SLP",
    "ENJ",
    "ETC",
    "LON",
    "TCT",
    "SKL",
    "CTXC",
    "MXC",
    "ICP",
    "SAITAMA",
    "MYRIA",
    "CVC",
    "LRC",
    "POR",
    "GF",
    "THETA",
    "COMP",
    "RVN",
    "ELON",
    "MDA",
    "XEC",
    "VRA",
    "HBAR",
    "RFUEL",
    "ENS",
    "NEAR",
    "ORB",
    "MCO",
    "GALA",
    "KSM",
    "ZIL",
    "LTC",
    "UNI",
    "EOS",
    "BADGER",
    "METIS",
    "NULS",
    "XETA",
    "CVP",
    "IMX",
    "MILO",
    "FIL",
    "DAO",
    "PRQ",
    "ETHW",
    "SOL",
    "STORJ",
    "GEAR",
    "OXT",
    "AERGO",
    "DHT",
    "SKEB",
    "AST",
    "RADAR",
    "BLUR",
    "MENGO",
    "FRONT",
    "STC",
    "LDO",
    "LUNC",
    "GLM",
    "DYDX",
    "GHST",
    "ARG",
    "FORTH",
    "ICX",
    "APT",
    "VSYS",
    "APE",
    "OM",
    "REP",
    "SWEAT",
    "TRB",
    "ACA",
    "XEM",
    "BORA",
    "KISHU",
    "ASTR",
    "LSK",
    "WING",
    "AKITA",
    "ARB",
    "IQ",
    "ZYRO",
    "XPR",
    "NMR",
    "SNT",
    "GAL",
    "GODS",
    "KINE",
    "CHE",
    "OP",
    "JFI",
    "KP3R",
    "WIFI",
    "KNC",
    "WAXP",
    "WOO",
    "REVV",
    "MAGIC",
    "POLS",
    "IGU",
    "LAT",
    "MINA",
    "YGG",
    "CELO",
    "ORBS",
    "USTC",
    "XNO",
    "OAS",
    "LUNA",
    "MOVEZ",
    "AUCTION",
    "POLYDOGE",
    "TON",
    "APIX",
    "FTM",
    "PERP",
    "SC",
    "ERN",
    "OMI",
    "WGRT",
    "ID",
    "MOVR",
    "ZEC",
    "KAR",
    "QOM",
    "FLR",
    "GMX",
    "ALCX",
    "T",
    "ONE",
    "GM",
    "LITH",
    "UMEE",
    "LEO",
    "VALUE",
    "CLV",
    "PCI",
    "SIS",
    "PHA",
    "STARL",
    "THG",
    "KCAL",
    "DIA",
    "CTC",
    "FITFI",
    "RDNT",
    "BAND",
    "BABYDOGE",
    "LEASH",
    "PIT",
    "UMA",
    "ANC",
    "API3",
    "OMG",
    "EFI",
    "STX",
    "LOOKS",
    "SWFTC",
    "FLOKI",
    "CSPR",
    "SOS",
    "GFT",
    "BORING",
    "DOME",
    "BICO",
    "CONV",
    "CITY",
    "SUI",
    "VELA",
    "LOON",
    "SRM",
    "HEGIC",
    "RIO",
    "MASK",
    "MIR",
    "AIDOGE",
    "CETUS",
    "BRWL",
    "PEPE",
    "KOL",
    "LET",
    "DOSE",
    "WSB",
    "DMD",
    "GALFT",
    "ORDI",
    "LHINU",
)


# coins = coins[:5]


def main_not_async(to: str):
    asyncio.run(process_coin(to))


async def process_coin(to):
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=10, decode_responses=True)
    counter = int(redis_client.get('counter') if redis_client.get('counter') else 0)
    print("Counter", counter)
    if counter >= 1:
        print("To much exit")
        return

    try:
        _rate, _type, _, qd1 = await get_exchange_rate("USDT", to)
        first_amount = print_rate(_rate, _type, 20, "USDT", to)
        if float(_rate) > 0:
            for _to in coins:
                una = await crud.unavailable.get_from_ccy_to_ccy(db=db, from_ccy=to, to_ccy=_to)
                if una:
                    continue
                try:
                    from_to_rate, from_to_type, _, qd2 = await get_exchange_rate(to, _to)
                    if float(from_to_rate) > 0:
                        second_amount = print_rate(from_to_rate, from_to_type, first_amount, to, _to)
                        una = await crud.unavailable.get_from_ccy_to_ccy(db=db, from_ccy="USDT", to_ccy=_to)
                        if una:
                            continue
                        try:
                            to_rate, to_type, _, qd3 = await get_exchange_rate(_to, "USDT", "sell")
                            if float(to_rate) > 0:
                                print_rate(to_rate, to_type, second_amount, _to, "USDT")
                                c = coef(1, _rate, _type, from_to_rate, from_to_type, to_rate, to_type)
                                data = f"USDT|{_rate}|{to}|{from_to_rate}|{_to}|{to_rate}|USDT {c}"
                                if 1 < c < 1.03:
                                    await process(data, redis_client)
                            else:
                                await crud.unavailable.create(db=db, obj_in={"from_ccy": "USDT", "to_ccy": _to})
                                continue
                        except Exception as e:
                            print("Exception in third line")
                            print(e)
                except Exception as e:
                    print("Exception in second line")
                    print(e)
                else:
                    await crud.unavailable.create(db=db, obj_in={"from_ccy": to, "to_ccy": _to})
                    continue
    except Exception as e:
        print("Exception if first line")
        print(e)


def print_rate(rate, _type, amount, from_ccy, to_ccy):
    converted_amount = amount / float(rate) if _type == "buy" else amount * float(rate)
    print(f" Rate 1 {rate} {from_ccy}->{to_ccy} = 20->{converted_amount}")
    return converted_amount


async def process(data, redis_client):
    cs = data.split(" ")[0].split("|")
    from_usdt = float(wait_currency("USDT"))
    _rate, _type, q1, qd1 = await get_exchange_rate(cs[0], cs[2], amount=from_usdt)

    if _type == "buy":
        first_amount = float(from_usdt) / float(_rate)
    else:
        first_amount = float(from_usdt) * float(_rate)
    from_to_rate, from_to_type, q2, qd2 = await get_exchange_rate(cs[2], cs[4], amount=first_amount)

    if from_to_type == "buy":
        second_amount = float(first_amount) / float(from_to_rate)
    else:
        second_amount = float(first_amount) * float(from_to_rate)
    to_rate, to_type, q3, qd3 = await get_exchange_rate(cs[4], cs[6], "sell", amount=second_amount)

    c = coef(1, _rate, _type, from_to_rate, from_to_type, to_rate, to_type)
    if c > 1:
        #print(data + " -> " + str(c))

        redis_client.incr('counter')
        counter = int(redis_client.get('counter'))

        send_email("Rich", data + " -> " + str(c) + "\n" + q1 + "\n" + q2 + "\n" + q3)
        #  await exchange_crypto(cs[2], cs[4], q1, q2, q3, _type, from_to_type, to_type, qd1, qd2, qd3)

        if counter <= 1:
            return "Boo"


async def exchange_crypto(first, second, q1, q2, q3, t1, t2, t3, qd1, qd2, qd3):
    print(f" --- {first} {second} {q1} {q2} {q3} {t1} {t2} {t3}")
    print("Q1: ", qd1)
    print("Q2: ", qd2)
    print("Q3: ", qd3)
    convert1 = convert2 = None
    try:
        from_usdt = wait_currency("USDT")
        if from_usdt > 0:
            print(f"  00. First quota data {qd1['baseCcy']} {qd1['quoteCcy']} {qd1['rfqSz']} {qd1['side']}")
            print(f"  0. Convert from baseCcy={qd1['baseCcy']}[USDT] to quotaCcy={qd1['quoteCcy']}[{first}] {qd1['rfqSz']}")
            convert1 = convert(from_ccy=qd1['baseCcy'], to_ccy=qd1['quoteCcy'], amount=from_usdt, quote_id=q1, side=t1)
            print(convert1)
            sleep(0.071)

        first_amount = wait_currency(first)
        if first_amount > 0:
            print(f"  00. Second quota data {qd2['baseCcy']} {qd2['quoteCcy']} {qd2['rfqSz']} {qd2['side']}")
            print(f"  0. Convert from baseCcy={qd2['baseCcy']}[{first}] to quotaCcy={qd2['quoteCcy']}[{second}]")
            convert2 = convert(from_ccy=qd2['baseCcy'], to_ccy=qd2['quoteCcy'], amount=first_amount, quote_id=q2,
                               side=t2)
            print(convert2)
            sleep(0.071)

        second_amount = wait_currency(second)
        if second_amount > 0:
            print(f"  00. Third quota data {qd3['baseCcy']} {qd3['quoteCcy']} {qd3['rfqSz']} {qd3['side']}")
            print(f"  0. Convert from baseCcy={qd2['baseCcy']}[{second}] to quotaCcy={qd2['quoteCcy']}[USDT]")
            convert3 = convert(from_ccy=qd3['baseCcy'], to_ccy=qd3['quoteCcy'], amount=second_amount, quote_id=q3,
                               side=t3)
            print(convert3)

        to_usdt = wait_currency("USDT")
        print(f"USDT {from_usdt:.4f} -> {to_usdt:.4f}")

    except Exception as e:
        print("Exception in exchange")
        print(e)

        if convert1["code"] == "58009":
            first_amount = wait_currency(first)
            price, side, quota_id = await get_exchange_rate(first, "USDT", "buy", first_amount)
            convert_back1 = convert(first, "USDT", first_amount, quota_id)
            print("Convert back 1", convert_back1)
            return "Ohho"

        if convert2["code"] == "58009":
            second_amount = wait_currency(second)
            price, side, quota_id = await get_exchange_rate(first, "USDT", "buy", second_amount)
            convert_back2 = convert(first, "USDT", second_amount, quota_id)
            print("Convert back 2", convert_back2)
            return "Ohho"


def convert(from_ccy, to_ccy, amount, quote_id, side="buy"):
    okx = OKX()
    print(f"  1. Convert from {from_ccy} to {to_ccy} {amount}")
    return okx.convert(from_ccy=from_ccy, to_ccy=to_ccy, amount=amount, quoteId=quote_id, side=side)


def wait_currency(ccy):
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    c = None
    while c is None:
        currency = okx.get_account_balance(ccy, settings.OKX_API_KEY, settings.OKX_SECRET_KEY, settings.OKX_PASSPHRASE)

        if len(currency["data"]) == 0:
            c = None
        else:
            c = currency["data"][0]["availBal"]
        sleep(0.05)

    return float(c)


def coef(c, _rate, _type, from_to_rate, from_to_type, to_rate, to_type):
    if _type == "buy":
        c = float(c) / float(_rate)
    else:
        c = float(c) * float(_rate)

    if from_to_type == "buy":
        c = float(c) / float(from_to_rate)
    else:
        c = float(c) * float(from_to_rate)

    if to_type == "buy":
        c = float(c) / float(to_rate)
    else:
        c = float(c) * float(to_rate)

    return c


def send_email(subject, message):
    sender_email = "info@mongo.one"
    receiver_email = "dg@mongo.one"
    smtp_server = "mongo.one"
    smtp_port = 25
    headers = f"From: {sender_email}\r\nTo: {receiver_email}\r\nSubject: {subject}\r\n\r\n"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.sendmail(sender_email, receiver_email, headers + message)


async def get_proxy():
    proxy = []
    async for p in db["proxy"].find({"$query": {}, "$orderby": {"used": 1}}).skip(0).limit(1):
        proxy = p

    db["proxy"].update_one(
        {"_id": proxy["_id"]}, {"$set": {"used": datetime.now()}}  # type: ignore
    )
    return {"http": f"{proxy.get('host')}:{proxy.get('port')}"}


async def get_exchange_rate(from_coin, to_coin, side="buy", amount=1.0):
    try:
        una = await crud.unavailable.get_from_ccy_to_ccy(db=db, from_ccy=from_coin, to_ccy=to_coin)
        if una:
            return 0, una, None, None
        okx = OKX()
        price, side, quote_id, data = okx.get_exchange_info(from_coin=from_coin, to_coin=to_coin, side=side,
                                                            amount=amount)
        if price == -1:
            await crud.unavailable.create(db=db, obj_in={"from_ccy": from_coin, "to_ccy": to_coin})
            return 0, una, None, None
        return price, side, quote_id, data
    except Exception as e:
        print("Exception in get exchange rate")
        print(e)
        exit(1)


if __name__ == "__main__":
    # first = "TRX"
    # second = "XRP"
    # q1 = "quoternext2TRX-USDT16926090858816031"
    # q2 = "quoter2TRX-XRP16926090862592069"
    # q3 = "quoternext2XRP-USDT16926090866266035"
    # t1 = "buy"
    # t2 = "buy"
    # t3 = "buy"
    # from_usdt = wait_currency("USDT")
    # convert1 = convert(from_ccy="USDT", to_ccy=first, amount=from_usdt, quote_id=q1, side=t1)
    # first_amount = wait_currency(first)
    # print(f"first amount {first_amount:.4f}")
    # convert2 = convert(from_ccy=first, to_ccy=second, amount=first_amount, quote_id=q2, side=t2)
    # second_amount = wait_currency(second)
    # print(f"second amount {second_amount:.4f}")
    # convert3 = convert(from_ccy=second, to_ccy="USDT", amount=second_amount, quote_id=q3, side=t3)
    # to_usdt = wait_currency("USDT")
    # print(f"USDT {from_usdt:.4f} -> {to_usdt:.4f}")

    typer.run(main_not_async)
