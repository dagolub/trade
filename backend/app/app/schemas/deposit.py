from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepositBase(BaseModel):
    wallet: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    callback: Optional[str] = None
    callback_response: Optional[str] = ""
    sum: float = None  # type: ignore
    currency: str = None  # type: ignore
    chain: str = None  # type: ignore
    created: Optional[datetime]


class DepositCreate(DepositBase):
    owner_id: Optional[str] = None
    sub_account: Optional[str] = None
    sub_account_label: Optional[str] = None
    sub_account_secret_key: Optional[str] = None
    sub_account_api_key: Optional[str] = None
    sub_account_passphrase: Optional[str] = None


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
