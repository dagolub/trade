from sqlalchemy import Boolean, Column, Integer, String, func  # type: ignore
from trade.db.utcdatetime import UtcDateTime
from trade.db.base_class import Base


class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean(), default=True)

    added = Column(UtcDateTime, server_default=func.now())
