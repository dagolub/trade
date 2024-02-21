from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    hashed_password: str
    is_active: bool


class CustomerUpdate(BaseModel):
    name: str
    hashed_password: str
    is_active: bool


# Properties shared by models stored in DB
class CustomerInDB(CustomerCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class Customer(CustomerInDB):
    pass
