from typing import Generic, Type, TypeVar, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from trade.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId  # type: ignore

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: Session, id: str) -> Optional[ModelType]:
        current_user = await db[self.model.__tablename__].find_one({"_id": ObjectId(id)})  # type: ignore
        if current_user:
            current_user["id"] = str(current_user["_id"])
            return current_user
        else:
            return None

    async def create(self, db: Session, obj_in: dict) -> Optional[ModelType]:
        print(f"Add to unavailable {obj_in['from_ccy']} {obj_in['to_ccy']}")
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

    async def count(self, db: Session):  # type: ignore
        return await db[self.model.__tablename__].count_documents({})  # type: ignore

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = []
        async for document in db[self.model.__tablename__].find().skip(skip).limit(limit):  # type: ignore
            document["id"] = str(document["_id"])  # noqa
            result.append(document)
        return result