from sqlalchemy import Column, Integer, String, Float, ForeignKey  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from trade.db.base_class import Base
from trade.db.utcdatetime import UtcDateTime


class Operation(Base):
    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer", foreign_keys=[customer_id])

    start_balance = Column(Integer)

    local_exchanger = Column(String)
    local_from_currency = Column(String)
    local_from_amount = Column(Integer)
    local_from_address_id = Column(Integer, ForeignKey("address.id"))
    local_from_address = relationship("Address", foreign_keys=[local_from_address_id])
    local_to_currency = Column(String)
    local_to_amount = Column(Integer)
    local_to_address_id = Column(Integer, ForeignKey("address.id"))
    local_to_address = relationship("Address", foreign_keys=[local_to_address_id])

    transfer_fee = Column(Integer)

    foreign_exchanger = Column(String)
    foreign_from_currency = Column(String)
    foreign_from_amount = Column(Integer)
    foreign_from_address_id = Column(Integer, ForeignKey("address.id"))
    foreign_from_address = relationship(
        "Address", foreign_keys=[foreign_from_address_id]
    )
    foreign_to_currency = Column(String)
    foreign_to_amount = Column(Integer)
    foreign_to_address_id = Column(Integer, ForeignKey("address.id"))
    foreign_to_address = relationship("Address", foreign_keys=[foreign_to_address_id])

    transfer_back_fee = Column(Integer)

    final_balance = Column(Integer)

    profit = Column(Float)

    added = Column(UtcDateTime)
