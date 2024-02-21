from pydantic import BaseModel
from datetime import datetime


class VolatilityCreate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


class VolatilityUpdate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


# Properties shared by models stored in DB
class VolatilityInDB(VolatilityCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class Volatility(VolatilityInDB):
    pass
