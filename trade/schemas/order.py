from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderCreate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    buy_price: float
    sell_price: Optional[float] = 0
    status: str
    start_coin: float
    finish_coin: Optional[float] = 0
    profit: Optional[float] = 0
    profit_usd: Optional[float] = 0

    added: datetime
    updated: Optional[datetime] = None


class OrderUpdate(BaseModel):
    customer_id: Optional[int]

    from_coin: Optional[str]
    to_coin: Optional[str]
    buy_price: Optional[float]
    sell_price: float = 0
    status: str
    start_coin: Optional[float]
    finish_coin: float = 0
    profit: float = 0
    profit_usd: Optional[float] = 0

    added: Optional[datetime]
    updated: datetime


# Properties shared by models stored in DB
class OrderInDB(OrderCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class Order(OrderInDB):
    pass
