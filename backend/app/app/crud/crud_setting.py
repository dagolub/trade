from typing import TypeVar

from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDSetting(CRUDBase[Setting, SettingCreate, SettingUpdate]):
    pass


setting = CRUDSetting(Setting)
