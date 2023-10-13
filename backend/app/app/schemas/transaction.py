from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    from_wallet: Optional[str] = None
    to_wallet: Optional[str] = None
    tx: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    type: Optional[str] = None
    created: Optional[datetime]


class TransactionCreate(TransactionBase):
    owner_id: Optional[str] = None
    deposit_id: Optional[str] = None


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
