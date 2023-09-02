from app.db.base_class import Base
from sqlalchemy import Column, String, DateTime  # type: ignore


class Wallet(Base):
    __tablename__ = "wallet"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    wallet = Column(String, index=True)
    type = Column(String)
    created = Column(DateTime)
