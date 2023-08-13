from typing import Dict
from pydantic import BaseModel


class SettingBase(BaseModel):
    data: Dict[str, str]


class SettingCreate(SettingBase):
    pass


class SettingUpdate(SettingBase):
    pass


class SettingInDBBase(SettingBase):
    id: str
    _id: str
    
    class Config:
        orm_mode = True


class Setting(SettingInDBBase):
    pass


class SettingInDB(SettingInDBBase):
    pass
