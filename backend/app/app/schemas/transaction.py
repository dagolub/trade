from typing import Optional
from pydantic import BaseModel
from bson.objectid import ObjectId


class TransactionBase(BaseModel):
    owner_id: Optional[str] = None
    from_wallet: Optional[str] = None
    to_wallet: Optional[str] = None
    tx: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[str] = None
    type: Optional[str] = None
    deposit_id: Optional[str] = None

    
class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDBBase(TransactionBase):
    id: str
    _id: str
    
    class Config:
        orm_mode = True


class Transaction(TransactionInDBBase):
    pass


class TransactionInDB(TransactionInDBBase):
    pass