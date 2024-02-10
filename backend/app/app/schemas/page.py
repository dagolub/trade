from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PageBase(BaseModel):
    owner_id: Optional[str]
    title: str
    description: Optional[str] = 0
    file: str = 0
    created: Optional[datetime]


class PageCreate(PageBase):
    pass


class PageUpdate(PageBase):
    pass


class PageInDBBase(PageBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Page(PageInDBBase):
    pass


class PageInDB(PageInDBBase):
    pass


class PageBaseCreate(PageBase):
    sum: float = None
    currency: str = None
    chain: str = None
    callback: str = None
