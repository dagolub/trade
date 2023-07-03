from typing import Optional
import datetime
from pydantic import BaseModel


# Shared properties
class TransactionBase(BaseModel):
    

# Properties to receive on Transaction creation
class TransactionCreate(TransactionBase):
    pass


# Properties to receive on Transaction update
class TransactionUpdate(TransactionBase):
    pass


# Properties shared by models stored in DB
class TransactionInDBBase(TransactionBase):
    id: int
    
    class Config:
        orm_mode = True


# Properties to return to client
class Transaction(TransactionInDBBase):
    pass


# Properties properties stored in DB
class TransactionInDB(TransactionInDBBase):
    pass