from typing import Optional
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel


class WithdrawBase(BaseModel):
    to: Optional[str] = None
    sum: Optional[int] = None
    created: Optional[datetime] = None


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
