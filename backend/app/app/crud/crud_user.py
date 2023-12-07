from typing import Any, Dict, Optional, TypeVar, Union
from datetime import datetime
from bson.objectid import ObjectId  # type: ignore
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app import crud
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

ModelType = TypeVar("ModelType", bound=Base)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: Session, email: str) -> Optional[User]:
        user = await db["user"].find_one({"email": email})
        if user:  # type: ignore
            user["id"] = str(user["_id"])
        return user

    async def create(self, db: Session, obj_in: dict) -> User:
        obj_in = jsonable_encoder(obj_in)
        db_obj = {
            "email": obj_in["email"],
            "hashed_password": get_password_hash(obj_in["password"]),
            "full_name": obj_in.get("full_name"),
            "is_superuser": obj_in.get("is_superuser") or False,
            "is_active": True,
            "created": datetime.utcnow(),
        }
        obj = await db[self.model.__tablename__].insert_one(document=db_obj)  # type: ignore
        user = await db[self.model.__tablename__].find_one(  # type: ignore
            {"_id": ObjectId(obj.inserted_id)}
        )  # type: ignore
        user["id"] = str(obj.inserted_id)
        return user

    async def update(  # noqa: 901
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]  # type: ignore
    ) -> User:
        update_data = await crud.user.get(db=db, entity_id=db_obj["id"])
        if type(obj_in) != dict:  # noqa
            obj_in = dict(obj_in)
        if "email" in update_data:
            del update_data["email"]  # type: ignore

        if "email" in obj_in:
            update_data["email"] = obj_in["email"]


        if "password" in obj_in and obj_in["password"] != "":  # type: ignore
            hashed_password = get_password_hash(obj_in["password"])  # type: ignore
            del obj_in["password"]  # type: ignore
            update_data["hashed_password"] = hashed_password  # type: ignore

        if "full_name" in obj_in:
            update_data["full_name"] = obj_in["full_name"]

        if "is_superuser" in obj_in:
            update_data["is_superuser"] = obj_in["is_superuser"]

        if "is_active" in obj_in:
            update_data["is_active"] = obj_in["is_active"]


        if "autotransfer" in obj_in:
            update_data["autotransfer"] = obj_in["autotransfer"]

        if "bal" in obj_in:
            update_data["bal"] = obj_in["bal"]

        if "commissions" in obj_in:
            update_data["commissions"] = obj_in["commissions"]

        await db[self.model.__tablename__].update_one({"_id": ObjectId(db_obj["id"])}, {"$set": update_data})  # type: ignore
        user = await db[self.model.__tablename__].find_one({"_id": ObjectId(db_obj["id"])})  # type: ignore
        user["id"] = str(user["_id"])
        return user

    async def authenticate(
        self, db: AsyncIOMotorClient, *, email: str, password: str
    ) -> Optional[User]:
        current_user = await self.get_by_email(db, email=email)
        if not current_user:
            return None
        if not verify_password(password, current_user["hashed_password"]):  # type: ignore
            return None
        return current_user

    @staticmethod
    def is_active(current_user: User) -> bool:
        return current_user["is_active"]  # type: ignore

    @staticmethod
    def is_superuser(current_user: User) -> bool:
        return current_user["is_superuser"]  # type: ignore


user = CRUDUser(User)
