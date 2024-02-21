from pydantic import BaseModel


class TransactionCreate(BaseModel):
    customer_id: int

    from_exchanger: str
    from_address_id: int

    to_exchanger: str
    to_address_id: int
    amount: int
    coin: str
    chain: str
    network_fee: int
    tx_id: str


class TransactionUpdate(BaseModel):
    customer_id: int

    from_exchanger: str
    from_address_id: int

    to_exchanger: str
    to_address_id: int

    coin: str
    chain: str
    network_fee: int
    tx_id: str


# Properties shared by models stored in DB
class TransactionInDB(TransactionCreate):
    id: int

    class Config:
        orm_mode: True  # type: ignore


# Properties to return to admins
class Transaction(TransactionInDB):
    pass
