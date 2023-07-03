from typing import Optional
import datetime
from pydantic import BaseModel


# Shared properties
class DepositBase(BaseModel):
    

# Properties to receive on Deposit creation
class DepositCreate(DepositBase):
    pass


# Properties to receive on Deposit update
class DepositUpdate(DepositBase):
    pass


# Properties shared by models stored in DB
class DepositInDBBase(DepositBase):
    id: int
    
    class Config:
        orm_mode = True


# Properties to return to client
class Deposit(DepositInDBBase):
    pass


# Properties properties stored in DB
class DepositInDB(DepositInDBBase):
    pass