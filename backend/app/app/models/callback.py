from sqlalchemy import Column, String, Integer  # type: ignore

from app.db.base_class import Base


class Callback(Base):
    __tablename__ = "deposits"
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    deposit_id = Column(String, index=True)
    callback = Column(String)
    callback_response = Column(String)
