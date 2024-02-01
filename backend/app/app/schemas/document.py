from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DocumentBase(BaseModel):
    owner_id: str = None
    name: Optional[str] = ""
    file: Optional[str] = ""
    ext: Optional[str] = ""
    folder_id: Optional[int] = 0
    created: Optional[datetime] = ""


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(DocumentBase):
    pass


class DocumentInDBBase(DocumentBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Document(DocumentInDBBase):
    pass


class DocumentInDB(DocumentInDBBase):
    pass


class DocumentBaseCreate(DocumentBase):
    sum: float = None
    currency: str = None
    chain: str = None
    callback: str = None
