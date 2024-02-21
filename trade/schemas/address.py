from pydantic import BaseModel


class AddressCreate(BaseModel):
    customer_id: int

    exchanger: str
    coin: str
    chain: str
    address: str


class AddressUpdate(BaseModel):
    customer_id: int

    exchanger: str
    coin: str
    chain: str
    address: str


# Properties shared by models stored in DB
class AddressInDB(AddressCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class Address(AddressInDB):
    pass
