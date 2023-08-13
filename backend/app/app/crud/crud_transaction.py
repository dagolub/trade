from app.crud.base import CRUDBase
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.db.base_class import Base
from typing import TypeVar, List
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    async def get_not_filled(
        self,
        mongo_db: Session,
    ) -> List[ModelType]:
        result = []

        async for document in mongo_db[self.model.__tablename__].find({"tx": {"$regex": "^[0-9]+$"}}):  # type: ignore
            document["id"] = str(document["_id"])  # noqa

            result.append(document)

        return result


transaction = CRUDTransaction(Transaction)
