from sqlalchemy import Column, Integer, String  # type: ignore

from app.db.base_class import Base


class Transaction(Base):
    __tablename__ = "transaction"
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    from_wallet = Column(String, index=True)
    to_wallet = Column(String)
    tx = Column(String)
    amount = Column(Integer)
    currency = Column(String)
    type = Column(String)
    deposit_id = Column(String)
