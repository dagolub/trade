from trade.crud.base import CRUDBase
from trade.models.pair import Pair
from trade.schemas.pair import PairCreate, PairUpdate
from sqlalchemy.orm.session import Session  # type: ignore
from typing import Optional


class CRUDPair(CRUDBase[Pair, PairCreate, PairUpdate]):
    def get_by_start_send(self, db: Session, start: str, send: str) -> Optional[Pair]:
        return self.query(db, Pair.start_coin == start, Pair.send_coin == send).first()  # type: ignore


pair = CRUDPair(Pair)
