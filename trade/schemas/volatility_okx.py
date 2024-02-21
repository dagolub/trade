from pydantic import BaseModel
from datetime import datetime


class VolatilityOKXCreate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


class VolatilityOKXUpdate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


# Properties shared by models stored in DB
class VolatilityOKXInDB(VolatilityOKXCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class VolatilityOKX(VolatilityOKXInDB):
    pass
