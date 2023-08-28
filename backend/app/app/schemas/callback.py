from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class CallbackBase(BaseModel):
    owner_id: Optional[str] = None
    Callback_id: Optional[str] = None
    callback: Optional[str] = None
    callback_response: Optional[str] = None
    created: Optional[datetime]


class CallbackCreate(CallbackBase):
    pass


class CallbackUpdate(CallbackBase):
    pass


class CallbackInDBBase(CallbackBase):
    id: str
    _id: str

    class Config:
        orm_mode = True


class Callback(CallbackInDBBase):
    pass


class CallbackInDB(CallbackInDBBase):
    pass
