from app.crud.base import CRUDBase
from app.models.withdraw import Withdraw
from app.schemas.withdraw import WithdrawCreate, WithdrawUpdate
from sqlalchemy.orm import Session
from typing import Optional, TypeVar, Type
from app.db.base_class import Base
from datetime import datetime
from app.services.client import OKX
from app import crud


ModelType = TypeVar("ModelType", bound=Base)


class CRUDWithdraw(CRUDBase[Withdraw, WithdrawCreate, WithdrawUpdate]):
    okx = ""

    def __init__(self, model: Type[ModelType]):
        self.okx = OKX()
        super().__init__(model)

    def _get_min_withdraw(self, currencies: [], currency: str, chain: str):
        for c in currencies:
            if str(c["ccy"].lower()) == str(currency.lower()):

                _chain = self.okx.get_currency_chain(currency, chain)
                if c["chain"] == _chain:
                    if "minDep" in c:
                        return c["minWd"]

    async def create(
        self, db: Session, obj_in: dict, current_user=None
    ) -> Optional[ModelType]:
        currencies = self.okx.get_currencies()
        min_withdraw = self._get_min_withdraw(
            currencies["data"], str(obj_in.currency), str(obj_in.chain)
        )
        if float(obj_in.sum) < float(min_withdraw):
            raise ValueError(
                f"Min withdraw in {obj_in.currency} {obj_in.chain} is {min_withdraw}"
            )

        user = await crud.user.get(db=db, entity_id=current_user["id"])
        comm = {"percent": 0, "fixed": 0}
        if (
            "commissions" in user
            and obj_in.currency.lower() in user["commissions"]  # noqa
            and "out" in user["commissions"][obj_in.currency.lower()]  # noqa
        ):
            comm = user["commissions"][obj_in.currency.lower()]["out"]
        fee = float(obj_in.sum) * 0.0100 * float(comm["percent"]) + float(comm["fixed"])
        status = "created"
        if "bal" in user and obj_in.currency in user["bal"]:
            if fee + obj_in.sum > user["bal"][obj_in.currency]:
                status = "Amount more than you have"


        obj_in = {
            "owner_id": current_user["id"],
            "sum": obj_in.sum,
            "to": obj_in.to,
            "callback": obj_in.callback,
            "currency": obj_in.currency.upper(),
            "chain": obj_in.chain.upper(),
            "fee": fee,
            "status": status,
            "network_fee": 0,
            "created": datetime.utcnow(),
        }

        return await super().create(db=db, obj_in=obj_in)


withdraw = CRUDWithdraw(Withdraw)
