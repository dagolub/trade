from typing import Optional
from pydantic import BaseModel
from bson.objectid import ObjectId


class DepositBase(BaseModel):
    owner_id: Optional[str] = None
    wallet: Optional[str] = None
    type: Optional[str] = None
    sum: Optional[int] = None
    currency: Optional[str] = None
    
    
class DepositCreate(DepositBase):
    pass


class DepositUpdate(DepositBase):
    pass


class DepositInDBBase(DepositBase):
    _id: ObjectId
    
    class Config:
        orm_mode = True


class Deposit(DepositInDBBase):
    pass


class DepositInDB(DepositInDBBase):
    pass