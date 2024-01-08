from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ApikeyBase(BaseModel):
    owner_id: Optional[str] = None
    apikey: Optional[str] = None
    deposit: Optional[bool] = False
    withdraw: Optional[bool] = False
    ips: Optional[str] = ""
    created: Optional[datetime]


class ApikeyCreate(ApikeyBase):
    id: Optional[str]


class ApikeyUpdate(ApikeyBase):
    id: str
    _id: str


class ApikeyInDBBase(ApikeyBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Apikey(ApikeyInDBBase):
    pass


class ApikeyInDB(ApikeyInDBBase):
    pass
