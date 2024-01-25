from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class QuotaBase(BaseModel):
    id: Optional[str]
    data: Optional[str]
    ttl: datetime


class QuotaCreate(QuotaBase):
    pass


class QuotaUpdate(QuotaBase):
    pass


class QuotaInDBBase(QuotaBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Quota(QuotaInDBBase):
    pass


class QuotaInDB(QuotaInDBBase):
    pass
