from trade.crud.base import CRUDBase
from trade.models.volatility import Volatility
from trade.schemas.volatility import VolatilityCreate, VolatilityUpdate
from typing import Optional
from sqlalchemy.orm.session import Session  # type: ignore


class CRUDVolatility(CRUDBase[Volatility, VolatilityCreate, VolatilityUpdate]):
    def get_by_from_to(
        self, db: Session, from_coin: str, to_coin: str
    ) -> Optional[Volatility]:
        return self.query(  # type: ignore
            db, Volatility.from_coin == from_coin, Volatility.to_coin == to_coin
        ).first()


volatility = CRUDVolatility(Volatility)
