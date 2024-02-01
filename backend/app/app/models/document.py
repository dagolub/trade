from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String  # type: ignore


class Document(Base):
    __tablename__ = "document"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    name = Column(String)
    file = Column(String)
    ext = Column(String)
    folder_id = Column(Integer)
    created = Column(DateTime)
