from pydantic import BaseModel


class TransactionBase(BaseModel):
    pass
    

class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDBBase(TransactionBase):
    id: int
    
    class Config:
        orm_mode = True


class Transaction(TransactionInDBBase):
    pass


class TransactionInDB(TransactionInDBBase):
    pass
