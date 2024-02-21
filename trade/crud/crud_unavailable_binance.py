from trade.crud.base import CRUDBase
from trade.models.unavailable_binance import UnavailableBinance
from trade.schemas.unavaible_binance import UnavailableBinanceCreate, UnavailableBinanceUpdate
from sqlalchemy.orm import Session
from typing import Optional


class CRUDUnavailableBinance(CRUDBase[UnavailableBinance, UnavailableBinanceCreate, UnavailableBinanceUpdate]):

    async def get_from_ccy_to_ccy(self, db: Session, from_ccy: str, to_ccy: str) -> Optional[UnavailableBinance]:
        async for unavailable in db[self.model.__tablename__].find({"from_ccy": from_ccy, "to_ccy": to_ccy}):
            return unavailable


unavailable_binance = CRUDUnavailableBinance(UnavailableBinance)
