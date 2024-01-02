from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepositBase(BaseModel):
    owner_id: str = None
    wallet: str = ""
    type: Optional[str] = ""
    status: Optional[str] = ""
    exchange: Optional[dict] = {}
    callback: Optional[str] = ""
    callback_response: Optional[str] = ""
    sum: float = None  # type: ignore
    currency: str = None  # type: ignore
    chain: str = None  # type: ignore
    paid: Optional[str] = ""  # type: ignore
    fee: Optional[str] = ""  # type: ignore
    created: Optional[datetime] = ""


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


class DepositBaseCreate(DepositBase):
    sum: float = None
    currency: str = None
    chain: str = None
    callback: str = None
