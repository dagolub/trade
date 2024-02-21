from trade.crud.base import CRUDBase
from trade.models.exchange_okx import ExchangeOKX
from trade.schemas.exchange_okx import ExchangeOKXCreate, ExchangeOKXUpdate
from sqlalchemy.orm import Session  # type: ignore
from typing import List


class CRUDExchangeOKX(CRUDBase[ExchangeOKX, ExchangeOKXCreate, ExchangeOKXUpdate]):
    @staticmethod
    async def create(db: Session, obj_in: List[ExchangeOKXCreate]) -> None:
        if len(obj_in) == 1:
            await db[ExchangeOKX.__tablename__].insert_one(document=obj_in[0].__dict__)
        else:
            await db[ExchangeOKX.__tablename__].insert_many(
                [i.__dict__ for i in obj_in]
            )

    @staticmethod
    async def remove(db, search):
        return await db[ExchangeOKX.__tablename__].delete_many(search)


exchange_okx = CRUDExchangeOKX(ExchangeOKX)
