from app.crud.base import CRUDBase
from app.models.withdraw import Withdraw
from app.schemas.withdraw import WithdrawCreate, WithdrawUpdate
from sqlalchemy.orm import Session
from typing import Optional, TypeVar
from app.db.base_class import Base
from datetime import datetime

ModelType = TypeVar("ModelType", bound=Base)


class CRUDWithdraw(CRUDBase[Withdraw, WithdrawCreate, WithdrawUpdate]):
    async def create(
        self, db: Session, obj_in: dict, current_user: dict
    ) -> Optional[ModelType]:
        obj_in = {
            "owner_id": current_user["id"],
            "sum": obj_in.sum,
            "to": obj_in.to,
            "callback": obj_in.callback,
            "currency": obj_in.currency,
            "chain": obj_in.chain,
            "status": "created",
            "created": datetime.utcnow(),
        }

        return await super().create(db=db, obj_in=obj_in)


withdraw = CRUDWithdraw(Withdraw)
