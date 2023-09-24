from app.crud.base import CRUDBase
from app.models.callback import Callback
from app.schemas.callback import CallbackCreate, CallbackUpdate


class CRUDCallback(CRUDBase[Callback, CallbackCreate, CallbackUpdate]):
    pass


callback = CRUDCallback(Callback)
