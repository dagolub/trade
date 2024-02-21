from sqlalchemy import Column, Integer, String, ForeignKey, func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from trade.db.base_class import Base


class UnavailableBinance(Base):
    __tablename__: str = "unavailable_binance"
    id = Column(Integer, primary_key=True, index=True)
    from_ccy = Column(String)
    to_ccy = Column(String)
