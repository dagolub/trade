from datetime import datetime

from pydantic import BaseModel


class ExchangeBase(BaseModel):
    deposit_id: str
    currency: str
    rate: float
    usdt: float
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
