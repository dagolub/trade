from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, func, Float  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from trade.db.base_class import Base
from trade.db.utcdatetime import UtcDateTime


class OrderStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    from_coin = Column(String)
    to_coin = Column(String)
    buy_price = Column(Float)
    sell_price = Column(Float)
    status = Column(String)
    start_coin = Column(Float)
    finish_coin = Column(Float)
    profit = Column(Float)
    profit_usd = Column(Float)

    added = Column(UtcDateTime, server_default=func.now())
    updated = Column(UtcDateTime, server_default=func.now())
