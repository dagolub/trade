from sqlalchemy import Column, String, Integer  # type: ignore

from app.db.base_class import Base


class Wallet(Base):
    __tablename__ = "wallet"
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    wallet = Column(String, index=True)
    type = Column(String)
