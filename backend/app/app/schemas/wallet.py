from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class WalletBase(BaseModel):
    wallet: Optional[str] = None
    type: Optional[str] = None
    created: Optional[datetime]


class WalletCreate(WalletBase):
    owner_id: Optional[str] = None
    deposit_id: Optional[str] = None


class WalletUpdate(WalletBase):
    pass


class WalletInDBBase(WalletBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Wallet(WalletInDBBase):
    pass


class WalletInDB(WalletInDBBase):
    pass
