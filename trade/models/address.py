from sqlalchemy import Column, Integer, String, ForeignKey, func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from trade.db.base_class import Base
from trade.db.utcdatetime import UtcDateTime


class Address(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    exchanger = Column(String)
    coin = Column(String)
    chain = Column(String)
    address = Column(String)

    added = Column(UtcDateTime, server_default=func.now())
