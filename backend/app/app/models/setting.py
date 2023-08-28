from app.db.base_class import Base
from sqlalchemy import Column, String  # type: ignore


class Setting(Base):
    __tablename__ = "setting"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    data = Column(String)
