from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FolderBase(BaseModel):
    owner_id: Optional[str]
    name: str
    folder_id: Optional[int] = 0
    created: Optional[datetime]


class FolderCreate(FolderBase):
    pass


class FolderUpdate(FolderBase):
    pass


class FolderInDBBase(FolderBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Folder(FolderInDBBase):
    pass


class FolderInDB(FolderInDBBase):
    pass


class FolderBaseCreate(FolderBase):
    sum: float = None
    currency: str = None
    chain: str = None
    callback: str = None
