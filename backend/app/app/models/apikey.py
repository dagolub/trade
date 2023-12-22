from sqlalchemy import Column, String, DateTime, Boolean  # type: ignore

from app.db.base_class import Base


class Apikey(Base):
    __tablename__ = "apikey"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    apikey = Column(String)
    deposit = Column(Boolean)
    withdraw = Column(Boolean)
    ips = Column(String)
    created = Column(DateTime)
