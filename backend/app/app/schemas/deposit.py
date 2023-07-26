from typing import Optional
from pydantic import BaseModel
from bson.objectid import ObjectId


class DepositBase(BaseModel):
    owner_id: Optional[str] = None
    wallet: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    sub_account: Optional[str] = None
    sub_account_label: Optional[str] = None
    sub_account_secret_key: Optional[str] = None
    sub_account_api_key: Optional[str] = None
    sub_account_passphrase: Optional[str] = None
    sum: float = None
    currency: str = None
    
    
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