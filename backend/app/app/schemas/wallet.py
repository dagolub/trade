from typing import Optional
import datetime
from pydantic import BaseModel


# Shared properties
class WalletBase(BaseModel):
    

# Properties to receive on Wallet creation
class WalletCreate(WalletBase):
    pass


# Properties to receive on Wallet update
class WalletUpdate(WalletBase):
    pass


# Properties shared by models stored in DB
class WalletInDBBase(WalletBase):
    id: int
    
    class Config:
        orm_mode = True


# Properties to return to client
class Wallet(WalletInDBBase):
    pass


# Properties properties stored in DB
class WalletInDB(WalletInDBBase):
    pass