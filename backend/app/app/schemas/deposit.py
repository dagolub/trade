from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepositBase(BaseModel):
    owner_id: Optional[str] = None
    wallet: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    exchange: dict = {}
    callback: Optional[str] = None
    callback_response: Optional[str] = ""
    sum: float = None  # type: ignore
    currency: str = None  # type: ignore
    chain: str = None  # type: ignore
    paid: str = None  # type: ignore
    fee: str = None  # type: ignore
    created: Optional[datetime]


class DepositCreate(DepositBase):
    sub_account: Optional[str] = None


class DepositUpdate(DepositBase):
    pass


class DepositInDBBase(DepositBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Deposit(DepositInDBBase):
    pass


class DepositInDB(DepositInDBBase):
    pass


class DepositBaseCreate(BaseModel):
    sum: float = None
    currency: str = None
    chain: str = None
    callback: str = None
