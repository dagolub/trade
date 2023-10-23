from app.crud.base import CRUDBase
from app.models.exchange import Exchange
from app.schemas.exhange import ExchangeCreate, ExchangeUpdate


class CRUDExchange(CRUDBase[Exchange, ExchangeCreate, ExchangeUpdate]):
    pass


exchange = CRUDExchange(Exchange)
