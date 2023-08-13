from sqlalchemy import Column, String, Integer  # type: ignore

from app.db.base_class import Base


class Deposit(Base):
    __tablename__ = "deposits"
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    wallet = Column(String, index=True)
    type = Column(String)
    sum = Column(Integer)
    status = Column(Integer)
    sub_account = Column(Integer)
    sub_account_label = Column(Integer)
    sub_account_api_key = Column(Integer)
    sub_account_secret_key = Column(Integer)
    sub_account_passphrase = Column(Integer)
    currency = Column(String)
    chain = Column(String)
    callback = Column(String)
    callback_response = Column(String)
