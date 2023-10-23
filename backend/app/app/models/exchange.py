from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Float, String  # type: ignore


class Exchange(Base):
    __tablename__ = "exchange"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    deposit_id = Column(String, index=True)
    currency = Column(String)
    rate = Column(Float)
    usdt = Column(Float)
    created = Column(DateTime)
