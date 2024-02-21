from pydantic import BaseModel


class UnavailableBinanceCreate(BaseModel):
    from_ccy: str
    to_ccy: str


class UnavailableBinanceUpdate(BaseModel):
    pass


class UnavailableBinanceInDB(UnavailableBinanceCreate):
    id: int

    class Config:
        orm_mode = True


class UnavailableBinance(UnavailableBinanceInDB):
    pass
