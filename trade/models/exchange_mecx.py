from sqlalchemy import Column, Integer, String, ForeignKey, func, Float  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from trade.db.base_class import Base
from trade.db.utcdatetime import UtcDateTime


class ExchangeMECX(Base):
    __tablename__: str = "exchange_mecx"  # type: ignore
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    from_coin = Column(String)
    to_coin = Column(String)
    price = Column(Float)
    rate = Column(Float)

    added = Column(UtcDateTime, server_default=func.now())
