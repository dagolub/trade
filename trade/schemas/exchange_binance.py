from pydantic import BaseModel
from datetime import datetime


class ExchangeBinanceCreate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


class ExchangeBinanceUpdate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


# Properties shared by models stored in DB
class ExchangeBinanceInDB(ExchangeBinanceCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class ExchangeBinance(ExchangeBinanceInDB):
    pass
