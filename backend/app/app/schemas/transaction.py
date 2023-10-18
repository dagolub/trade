from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    from_wallet: Optional[str] = None
    to_wallet: Optional[str] = None
    tx: Optional[str] = None
    amount: Optional[float] = 0
    currency: Optional[str] = None
    type: Optional[str] = None
    fee: Optional[float] = 0
    created: Optional[datetime]
    deposit_id: Optional[str] = None
    withdraw_id: Optional[str] = None


class TransactionCreate(TransactionBase):
    owner_id: Optional[str] = None


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
