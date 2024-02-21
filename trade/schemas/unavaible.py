from pydantic import BaseModel


class UnavailableCreate(BaseModel):
    from_ccy: str
    to_ccy: str


class UnavailableUpdate(BaseModel):
    pass


class UnavailableInDB(UnavailableCreate):
    id: int

    class Config:
        orm_mode = True


class Unavailable(UnavailableInDB):
    pass
