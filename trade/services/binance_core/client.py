import hashlib
import hmac
from decimal import Decimal
from operator import itemgetter
import time
from typing import Optional, Dict
from urllib.parse import quote_plus
import requests
from aiohttp import ContentTypeError
from trade.cron.compare_binance import coins
from trade.core.httpclient import http_session
from trade.core.logger import logger

from .schema import BinanceResponse, BinanceDepositAddress


def calculate_signature(secret: str, data: Dict) -> str:
    ordered_data = sorted(
        [(k, v) for k, v in data.items() if k != "signature"], key=itemgetter(0)
    )
    query_string = "&".join(
        ["=".join([quote_plus(f"{i}") for i in (k, v)]) for k, v in ordered_data]
    )
    m = hmac.new(secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256)
    return m.hexdigest()


BINANCE_DOMAINS = ["api", "api1", "api2", "api3"]
binance_domain_idx = 0


def binance_subdomain() -> str:
    global binance_domain_idx
    if binance_domain_idx >= len(BINANCE_DOMAINS):
        binance_domain_idx = 0
    binance_domain_idx += 1
    return BINANCE_DOMAINS[binance_domain_idx - 1]


async def binance_api_call(
    method: str,
    path: str,
    *,
    token: str,
    secret: str,
    data: Optional[Dict] = None,
) -> BinanceResponse:
    url = f"https://{binance_subdomain()}.binance.com/{path}"
    headers = {}
    if token:
        headers["X-MBX-APIKEY"] = token
    # Calculate signature
    kwargs = {}
    if data is not None:
        if secret:
            data["signature"] = calculate_signature(secret, data)
        if data and method.upper() in ["GET", "HEAD"]:
            kwargs["params"] = data
        else:
            kwargs["data"] = data

    async with http_session() as session:
        func = getattr(session, method.lower())
        logger.info("Calling the binance API: %s %s", method, url)
        async with func(url, headers=headers, **kwargs) as response:
            content = await response.text()
            logger.info(
                "Binance API at %s responded with %d %s", path, response.status, content
            )
            try:
                data = await response.json()
                if "success" not in data:
                    data["success"] = response.status == 200
            except (ValueError, ContentTypeError):
                logger.error("Unable to decode Binance API response: %s", content)
                data = None
            return BinanceResponse(
                status_code=response.status,
                data=data,
            )


async def binance_deposit_address(
    coin: str, network: str, *, token: str, secret: str
) -> Optional[BinanceDepositAddress]:
    response = await binance_api_call(
        "GET",
        "sapi/v1/capital/deposit/address",
        data={
            "coin": coin,
            "network": network,
            "timestamp": int(time.time() * 1000),
        },
        token=token,
        secret=secret,
    )
    if response.status_code != 200:
        return None

    return BinanceDepositAddress(**response.data)


async def binance_exchange_rate(symbol: str) -> Optional[Decimal]:
    url = f"https://www.binance.com/api/v3/ticker/price?symbol="
    response = requests.get(
        url=url + symbol,
    )
    for coin in coins:
        if coin in symbol:
            symbol
    if response.status_code == 400:
        new_symbol = symbol.replace("USDT","") + "USDT"
        response = requests.get(url=url+new_symbol)
        return Decimal(1/float(response.json()["price"]))
    if response.status_code == 200:
        return Decimal(response.json()["price"])
    return None


async def get_coins(token: str, secret: str) -> Optional[Decimal]:
    response = await binance_api_call(
        "GET", "sapi/v1/capital/config/getall", token=token, secret=secret
    )
    if response.status_code == 200:
        return Decimal(response.json()["price"])
    return None


async def get_fee(coin: str, token: str, secret: str) -> Optional[Decimal]:
    response = await binance_api_call(
        "GET",
        "sapi/v1/asset/tradeFee",
        data={"symbol": coin},
        token=token,
        secret=secret,
    )
    if response.status_code == 200:
        return response.data
    return None
