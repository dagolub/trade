from pydantic import BaseModel
from datetime import datetime


class VolatilityMECXCreate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


class VolatilityMECXUpdate(BaseModel):
    customer_id: int

    from_coin: str
    to_coin: str
    price: float
    added: datetime


# Properties shared by models stored in DB
class VolatilityMECXInDB(VolatilityMECXCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class VolatilityMECX(VolatilityMECXInDB):
    pass
