from pydantic import BaseModel


class PairCreate(BaseModel):
    from_exchanger: str

    start_coin: str
    send_coin: str
    receive_coin: str
    final_coin: str

    to_exchanger: str

    start_coin_amount: float
    send_coin_amount: float
    send_fee: float
    receive_coin_amount: float
    final_coin_amount: float
    backward_fee: float
    profit: float


class PairUpdate(BaseModel):
    from_exchanger: str

    start_coin: str
    send_coin: str
    receive_coin: str
    final_coin: str

    to_exchanger: str

    start_coin_amount: float
    send_coin_amount: float
    send_fee: float
    receive_coin_amount: float
    final_coin_amount: float
    backward_fee: float
    profit: float


# Properties shared by models stored in DB
class PairInDB(PairCreate):
    id: int

    class Config:
        orm_mode = True


# Properties to return to admins
class Pair(PairInDB):
    pass
