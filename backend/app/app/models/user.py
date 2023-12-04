from sqlalchemy import Boolean, Column, String, DateTime  # type: ignore

from app.db.base_class import Base


class User(Base):
    __tablename__ = "user"  # type: ignore
    _id = Column(String, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bal = Column(String)
    commissions = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    autotransfer = Column(Boolean(), default=False)
    created = Column(DateTime)
