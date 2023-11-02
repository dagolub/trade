from app.crud.base import CRUDBase
from app.models.withdraw import Withdraw
from app.schemas.withdraw import WithdrawCreate, WithdrawUpdate
from sqlalchemy.orm import Session
from typing import Optional, TypeVar, Type
from app.db.base_class import Base
from datetime import datetime
from app.services.client import OKX

ModelType = TypeVar("ModelType", bound=Base)


class CRUDWithdraw(CRUDBase[Withdraw, WithdrawCreate, WithdrawUpdate]):
    okx = ""

    def __init__(self, model: Type[ModelType]):
        self.okx = OKX()
        super().__init__(model)

    def _get_min_withdraw(self, currencies: [], currency: str, chain: str):
        for c in currencies:
            if str(c["ccy"]) == str(currency):
                _chain = self.okx.get_currency_chain(currency, chain)
                if c["chain"] == _chain:
                    if "minDep" in c:
                        return c["minWd"]

    async def create(
        self, db: Session, obj_in: dict, current_user: dict
    ) -> Optional[ModelType]:
        currencies = self.okx.get_currencies()
        min_withdraw = self._get_min_withdraw(
            currencies["data"], str(obj_in.currency), str(obj_in.chain)
        )
        if float(obj_in.sum) < float(min_withdraw):
            raise ValueError(
                f"Min withdraw in {obj_in.currency} {obj_in.chain} is {min_withdraw}"
            )
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
