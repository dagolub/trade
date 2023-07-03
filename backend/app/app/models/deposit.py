from sqlalchemy import Column, String, Integer  # type: ignore

from app.db.base_class import Base


class Deposit(Base):
    __tablename__ = "deposit"
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    wallet = Column(String, index=True)
    type = Column(String)
    sum = Column(Integer)
    currency = Column(String)
