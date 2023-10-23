from typing import Generic, List, Optional, Type, TypeVar
from bson.objectid import ObjectId  # type: ignore
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def count(self, db: Session, owner_id=False, search="") -> int:
        if search == "":
            search = {}
        if owner_id:
            if search != "":
                search.update({"owner_id": owner_id})
        if owner_id:
            return await db[self.model.__tablename__].count_documents(search)
        else:
            return await db[self.model.__tablename__].count_documents(search)  # type: ignore

    async def get(self, db: Session, entity_id: str) -> Optional[ModelType]:
        entity = await db[self.model.__tablename__].find_one({"_id": ObjectId(entity_id)})  # type: ignore
        if entity:
            entity["id"] = str(entity["_id"])
            if "amount" in entity:
                entity["amount"] = float(entity["amount"])
            return entity
        else:
            return None

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, search=""
    ) -> List[ModelType]:
        result = []
        if search == "":
            search = {}

        async for document in db[self.model.__tablename__].find(search).sort("created", -1).skip(skip).limit(limit):  # type: ignore
            document["id"] = str(document["_id"])  # noqa
            if "amount" in document:
                document["amount"] = float(document["amount"])
            result.append(document)

        return result

    async def get_multi_by_owner(
        self, db: Session, owner_id, skip: int = 0, limit: int = 100, search=""
    ) -> List[ModelType]:
        result = []
        if search == "":
            search = {}

        async for document in db[self.model.__tablename__].find(search).sort("created", -1).skip(skip).limit(limit):  # type: ignore
            document["id"] = str(document["_id"])  # noqa
            if "amount" in document:
                document["amount"] = float(document["amount"])
            result.append(document)

        return result

    async def create(self, db: Session, obj_in: dict) -> Optional[ModelType]:
        obj = await db[self.model.__tablename__].insert_one(document=obj_in)  # type: ignore
        object = await db[self.model.__tablename__].find_one(  # type: ignore
            {"_id": ObjectId(obj.inserted_id)}
        )  # type: ignore
        object["id"] = str(obj.inserted_id)
        return object

    async def update(
        self, db: Session, *, db_obj: Optional[ModelType], obj_in: Optional[ModelType]
    ) -> Optional[ModelType]:
        obj_in = jsonable_encoder(obj_in)
        update_data = obj_in

        await db[self.model.__tablename__].update_one({"_id": ObjectId(db_obj["id"])}, {"$set": update_data})  # type: ignore
        entity = await db[self.model.__tablename__].find_one({"_id": ObjectId(db_obj["id"])})  # type: ignore
        entity["id"] = str(entity["_id"])
        return entity

    async def remove(self, db: AsyncIOMotorClient, entity_id: str) -> None:
        entity = await db[self.model.__tablename__].find_one(
            {"_id": ObjectId(entity_id)}
        )
        if entity:
            entity["id"] = str(entity["_id"])
        await db[self.model.__tablename__].delete_one({"_id": ObjectId(entity_id)})
        return entity

    async def get_by_deposit(self, db, deposit_id):
        entity = await db[self.model.__tablename__].find_one({"deposit_id": deposit_id})  # type: ignore
        if entity:
            entity["id"] = str(entity["_id"])
            return entity
        else:
            return None

    async def get_by_tx(self, db, tx):
        entity = await db[self.model.__tablename__].find_one({"tx": tx})  # type: ignore
        if entity:
            entity["id"] = str(entity["_id"])
            return entity
        else:
            return None

    async def get_by_status(self, db, status):
        if not isinstance(status, (list)):
            status = [status]
        result = []
        async for instance in db[self.model.__tablename__].find(
            {"status": {"$in": status}}
        ):
            instance["id"] = str(instance["_id"])
            result.append(instance)
        return result

    async def get_by_regex(self, db, search):
        result = []
        async for instance in db[self.model.__tablename__].find(search):
            instance["id"] = str(instance["_id"])
            result.append(instance)
        return result
