from pydantic import BaseModel
from datetime import datetime


class ExchangeMECXCreate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    rate: float
    added: datetime


class ExchangeMECXUpdate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    rate: float
    added: datetime


# Properties shared by models stored in DB
class ExchangeMECXInDB(ExchangeMECXCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class ExchangeMECX(ExchangeMECXInDB):
    pass
