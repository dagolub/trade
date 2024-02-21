from trade.crud.base import CRUDBase
from trade.models.volatility_okx import VolatilityOKX
from trade.schemas.volatility_okx import VolatilityOKXCreate, VolatilityOKXUpdate
from typing import Optional
from sqlalchemy.orm.session import Session  # type: ignore


class CRUDVolatilityOKX(
    CRUDBase[VolatilityOKX, VolatilityOKXCreate, VolatilityOKXUpdate]
):
    def get_by_from_to(
        self, db: Session, from_coin: str, to_coin: str
    ) -> Optional[VolatilityOKX]:
        return self.query(  # type: ignore
            db, VolatilityOKX.from_coin == from_coin, VolatilityOKX.to_coin == to_coin
        ).first()


volatility_okx = CRUDVolatilityOKX(VolatilityOKX)
