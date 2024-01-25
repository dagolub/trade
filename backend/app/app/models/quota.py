from app.db.base_class import Base
from sqlalchemy import Column, DateTime, String  # type: ignore


class Quota(Base):
    __tablename__ = "quota"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    id = Column(String)
    data = Column(String)
    ttl = Column(DateTime)
