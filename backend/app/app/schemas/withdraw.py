from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel


class WithdrawBase(BaseModel):
    to: str
    sum: float
    created: Optional[datetime] = None
    callback: Optional[str] = None
    currency: str
    chain: str
    status: Optional[str] = None


class WithdrawCreate(WithdrawBase):
    owner_id: Optional[str] = None


class WithdrawUpdate(WithdrawBase):
    pass


class WithdrawInDBBase(WithdrawBase):
    _id: ObjectId

    class Config:
        orm_mode = True


class Withdraw(WithdrawInDBBase):
    pass


class WithdrawInDB(WithdrawInDBBase):
    pass


class WithdrawBaseCreated(BaseModel):
    to: Optional[str] = None
    sum: float = None
    callback: Optional[str] = None
    currency: str
    chain: str
