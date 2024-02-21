from trade.crud.base import CRUDBase
from trade.models.unavailable import Unavailable
from trade.schemas.unavaible import UnavailableCreate, UnavailableUpdate
from sqlalchemy.orm import Session
from typing import Optional


class CRUDUnavailable(CRUDBase[Unavailable, UnavailableCreate, UnavailableUpdate]):

    async def get_from_ccy_to_ccy(self, db: Session, from_ccy: str, to_ccy: str) -> Optional[Unavailable]:
        async for unavailable in db[self.model.__tablename__].find({"from_ccy": from_ccy, "to_ccy": to_ccy}):
            return unavailable


unavailable = CRUDUnavailable(Unavailable)
