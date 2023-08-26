from typing import Optional

from pydantic import BaseModel


class DepositBase(BaseModel):
    owner_id: Optional[str] = None
    deposit_id: Optional[str] = None
    callback: Optional[str] = None
    callback_response: Optional[str] = None


class DepositCreate(DepositBase):
    pass


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
