from pydantic import BaseModel
from datetime import datetime


class ExchangeOKXCreate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


class ExchangeOKXUpdate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


# Properties shared by models stored in DB
class ExchangeOKXInDB(ExchangeOKXCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class ExchangeOKX(ExchangeOKXInDB):
    pass
