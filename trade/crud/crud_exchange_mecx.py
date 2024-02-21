from trade.models.exchange_mecx import ExchangeMECX
from trade.schemas.exchange_mecx import ExchangeMECXCreate, ExchangeMECXUpdate
from typing import TypeVar, List
from sqlalchemy.orm import Session  # type: ignore
from trade.crud.base import CRUDBase
from trade.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDExchangeMECX(CRUDBase[ExchangeMECX, ExchangeMECXCreate, ExchangeMECXUpdate]):
    @staticmethod
    async def create(db: Session, obj_in: List[ExchangeMECXCreate]) -> None:
        if len(obj_in) == 1:
            await db[ExchangeMECX.__tablename__].insert_one(document=obj_in[0].__dict__)
        else:
            await db[ExchangeMECX.__tablename__].insert_many(
                [i.__dict__ for i in obj_in]
            )

    @staticmethod
    async def remove(db, search):
        return await db[ExchangeMECX.__tablename__].delete_many(search)


exchange_mecx = CRUDExchangeMECX(ExchangeMECX)
