from trade.crud.base import CRUDBase
from trade.models.order import Order
from trade.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    ...


order = CRUDOrder(Order)
