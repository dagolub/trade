from sqlalchemy import Column, String, DateTime, Integer  # type: ignore
from app.db.base_class import Base


class Withdraw(Base):
    __tablename__ = "withdraw"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    to = Column(String)
    sum = Column(Integer)
    callback = Column(String)
    currency = Column(String)
    chain = Column(String)
    fee = Column(String)
    network_fee = Column(String)
    status = Column(String)
    created = Column(DateTime)
