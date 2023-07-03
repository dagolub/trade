from typing import Generic, Type, TypeVar, Optional, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from bson.objectid import ObjectId  # type: ignore
from fastapi.encoders import jsonable_encoder
from app.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, id: str) -> Optional[ModelType]:
        current_user = await db[self.model.__tablename__].find_one({"_id": ObjectId(id)})  # type: ignore
        if current_user:
            current_user["id"] = str(current_user["_id"])
            return current_user
        else:
            return None

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = []
        async for document in db[self.model.__tablename__].find().skip(skip).limit(limit):  # type: ignore
            document["id"] = str(document["_id"])  # noqa
            result.append(document)
        return result

    async def create(self, db: Session, obj_in: dict) -> Optional[ModelType]:
        obj = await db[self.model.__tablename__].insert_one(document=db_obj)  # type: ignore
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

    async def remove(self, db: AsyncIOMotorClient, user_id: str) -> None:
        await db[self.model.__tablename__].delete_one({"_id": user_id})
