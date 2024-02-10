from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String  # type: ignore


class Page(Base):
    __tablename__ = "page"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    title = Column(String)
    description = Column(String)
    file = Column(String)
    created = Column(DateTime)
