from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ExchangeBase(BaseModel):
    deposit_id: Optional[str]
    owner_id: Optional[str]
    currency: Optional[str]
    rate: Optional[float]
    usdt: Optional[float]
    _from: Optional[str]
    _to: Optional[str]
    amount: Optional[float]
    result: Optional[float]
    quoteId: Optional[str]
    created: datetime


class ExchangeCreate(ExchangeBase):
    pass


class ExchangeUpdate(ExchangeBase):
    pass


class ExchangeInDBBase(ExchangeBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Exchange(ExchangeInDBBase):
    pass


class ExchangeInDB(ExchangeInDBBase):
    pass
