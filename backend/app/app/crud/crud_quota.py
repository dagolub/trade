from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.quota import Quota
from app.schemas.quota import QuotaCreate, QuotaUpdate


class CRUDQuota(CRUDBase[Quota, QuotaCreate, QuotaUpdate]):
    async def get_by_id(self, db, id):
        return await db[self.model.__tablename__].find_one({"id": id})  # type: ignore


quota = CRUDQuota(Quota)
