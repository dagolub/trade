from typing import Optional, Dict

from pydantic.main import BaseModel
from pydantic.networks import HttpUrl


class BinanceResponse(BaseModel):
    status_code: int
    data: Optional[Dict]


class BinanceDepositAddress(BaseModel):
    coin: Optional[str]
    network: Optional[str]
    address: Optional[str]
    tag: Optional[str]
    url: Optional[HttpUrl]
