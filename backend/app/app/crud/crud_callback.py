from typing import TypeVar

from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.callback import Callback
from app.schemas.callback import CallbackCreate, CallbackUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDCallback(CRUDBase[Callback, CallbackCreate, CallbackUpdate]):
    pass


callback = CRUDCallback(Callback)
