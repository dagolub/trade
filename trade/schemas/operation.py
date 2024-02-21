from pydantic import BaseModel
from typing import Optional


class OperationCreate(BaseModel):
    customer_id: int

    start_balance: int

    local_exchanger: str
    local_from_currency: str
    local_from_amount: int
    local_from_address_id: Optional[int] = 0
    local_to_currency: Optional[str] = ""
    local_to_amount: Optional[int] = 0
    local_to_address_id: Optional[int] = 0

    transfer_fee: Optional[int] = 0

    foreign_exchanger: Optional[str] = ""
    foreign_from_currency: Optional[str] = ""
    foreign_from_amount: Optional[int] = 0
    foreign_from_address_id: Optional[int] = 0
    foreign_to_currency: Optional[str] = ""
    foreign_to_amount: Optional[int] = 0
    foreign_to_address_id: Optional[int] = 0

    transfer_back_fee: Optional[int] = 0

    final_balance: Optional[int] = 0

    profit: Optional[float] = 0


class OperationUpdate(BaseModel):
    customer_id: int

    start_balance: int

    local_exchanger: str
    local_from_currency: str
    local_from_amount: int
    local_from_address_id: Optional[int] = 0
    local_to_currency: Optional[str] = ""
    local_to_amount: Optional[int] = 0
    local_to_address_id: Optional[int] = 0

    transfer_fee: Optional[int] = 0

    foreign_exchanger: Optional[str] = ""
    foreign_from_currency: Optional[str] = ""
    foreign_from_amount: Optional[int] = 0
    foreign_from_address_id: Optional[int] = 0
    foreign_to_currency: Optional[str] = ""
    foreign_to_amount: Optional[int] = 0
    foreign_to_address_id: Optional[int] = 0

    transfer_back_fee: Optional[int] = 0

    final_balance: Optional[int] = 0

    profit: Optional[float] = 0


# Properties shared by models stored in DB
class OperationInDB(OperationCreate):
    id: int

    class Config:
        orm_mode: True  # type: ignore


# Properties to return to admins
class Operation(OperationInDB):
    pass
