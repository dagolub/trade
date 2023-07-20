from typing import Generic, Type, TypeVar, Optional, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from bson.objectid import ObjectId  # type: ignore
import re
from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def count(self, db: Session) -> int:
        return await db[self.model.__tablename__].count_documents({})

    async def get(self, db: Session, entity_id: str) -> Optional[ModelType]:
        entity = await db[self.model.__tablename__].find_one({"_id": ObjectId(entity_id)})  # type: ignore
        if entity:
            entity["id"] = str(entity["_id"])
            return entity
        else:
            return None

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, q=""
    ) -> List[ModelType]:
        result = []
        search = {}
        if q != "":
            regex_pattern = re.compile(q)
            search = {"_id": {"$regex": regex_pattern}}

        async for document in db[self.model.__tablename__].find(search).skip(skip).limit(limit):  # type: ignore
            document["id"] = str(document["_id"])  # noqa
            result.append(document)
        return result

    async def create(self, db: Session, obj_in: dict) -> Optional[ModelType]:
        obj = await db[self.model.__tablename__].insert_one(document=jsonable_encoder(obj_in))  # type: ignore
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
        user = await db[self.model.__tablename__].find_one({"_id": ObjectId(db_obj["id"])})  # type: ignore
        user["id"] = str(user["_id"])
        return user

    async def remove(self, db: AsyncIOMotorClient, id: str) -> None:
        entity = await db[self.model.__tablename__].find_one({"_id": ObjectId(id)})
        if entity:
            entity["id"] = str(entity["_id"])
        await db[self.model.__tablename__].delete_one({"_id": ObjectId(id)})
        return entity
