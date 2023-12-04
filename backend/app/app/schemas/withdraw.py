from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class WithdrawBase(BaseModel):
    owner_id: Optional[str] = None
    to: str
    sum: float
    created: Optional[datetime] = None
    callback: Optional[str] = None
    currency: str
    chain: str
    fee: float
    network_fee: float
    status: Optional[str] = None


class WithdrawCreate(WithdrawBase):
    pass


class WithdrawUpdate(WithdrawBase):
    pass


class WithdrawInDBBase(WithdrawBase):
    id: str
    _id: str

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
