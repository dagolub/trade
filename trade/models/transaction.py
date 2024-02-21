from sqlalchemy import Column, Integer, String, ForeignKey, func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from trade.db.base_class import Base
from trade.db.utcdatetime import UtcDateTime


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    from_exchanger = Column(String)
    from_address_id = Column(Integer, ForeignKey("address.id"))
    from_address = relationship("Address", foreign_keys=[from_address_id])
    to_exchanger = Column(String)
    to_address_id = Column(Integer, ForeignKey("address.id"))
    to_address = relationship("Address", foreign_keys=[to_address_id])
    coin = Column(String)
    chain = Column(String)
    network_fee = Column(Integer)
    tx_id = Column(String)

    added = Column(UtcDateTime, server_default=func.now())
