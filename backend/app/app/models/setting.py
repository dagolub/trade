from sqlalchemy import Column, String, Integer  # type: ignore

from app.db.base_class import Base


class Setting(Base):
    __tablename__ = "setting"
    _id = Column(String, primary_key=True, index=True)
    data = Column(String)
