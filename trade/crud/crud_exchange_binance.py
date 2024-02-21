from trade.crud.base import CRUDBase
from trade.models.exchange_binance import ExchangeBinance
from trade.schemas.exchange_binance import ExchangeBinanceCreate, ExchangeBinanceUpdate
from sqlalchemy.orm import Session  # type: ignore
from typing import List, TypeVar
from pydantic import BaseModel

from trade.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDExchange(
    CRUDBase[ExchangeBinance, ExchangeBinanceCreate, ExchangeBinanceUpdate]
):
    @staticmethod
    async def create(db: Session, obj_in: List[ExchangeBinanceCreate]) -> None:
        if len(obj_in) == 1:
            await db[ExchangeBinance.__tablename__].insert_one(
                document=obj_in[0].__dict__
            )
        else:
            await db[ExchangeBinance.__tablename__].insert_many(
                [i.__dict__ for i in obj_in]
            )

    @staticmethod
    async def remove(db, search):
        return await db[ExchangeBinance.__tablename__].delete_many(search)

exchange_binance = CRUDExchange(ExchangeBinance)
