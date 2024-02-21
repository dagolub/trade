from trade.crud.base import CRUDBase
from trade.models.volatility_mecx import VolatilityMECX
from trade.schemas.volatility_mecx import VolatilityMECXCreate, VolatilityMECXUpdate
from typing import List, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder


class CRUDVolatilityMECX(
    CRUDBase[VolatilityMECX, VolatilityMECXCreate, VolatilityMECXUpdate]
):
    @staticmethod
    async def get_by_from_to(
        db: Session, from_coin: str, to_coin: str
    ) -> Optional[VolatilityMECX]:
        current_user = await db[VolatilityMECX.__tablename__].find_one(
            {"from_coin": from_coin, "to_coin": to_coin}
        )
        if current_user:
            current_user["id"] = str(current_user["_id"])
            return current_user
        else:
            return None

    @staticmethod
    async def create(db: Session, obj_in: List[VolatilityMECXCreate]) -> None:
        try:
            if len(obj_in) == 1:
                await db[VolatilityMECX.__tablename__].insert_one(
                    document=obj_in[0].__dict__
                )
            else:
                await db[VolatilityMECX.__tablename__].insert_many(
                    [i.__dict__ for i in obj_in]
                )
        except Exception as e:
            print(e)

    @staticmethod
    async def update(
        db: Session, *, db_obj: VolatilityMECX, obj_in: VolatilityMECXUpdate
    ) -> None:
        try:
            data = jsonable_encoder(obj_in)
            data["added"] = obj_in["added"]  # type: ignore
            await db[VolatilityMECX.__tablename__].update_one(
                {"_id": ObjectId(db_obj["id"])}, {"$set": data}  # type: ignore
            )
        except Exception as e:
            print(e)


volatility_mexc = CRUDVolatilityMECX(VolatilityMECX)
