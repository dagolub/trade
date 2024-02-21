from sqlalchemy import Column, Integer, String, Float  # type: ignore

from trade.db.base_class import Base


class Pair(Base):
    __tablename__ = "pair"
    id = Column(Integer, primary_key=True, index=True)

    from_exchanger = Column(String)

    start_coin = Column(String)
    send_coin = Column(String)
    receive_coin = Column(String)
    final_coin = Column(String)

    to_exchanger = Column(String)

    start_coin_amount = Column(Float)
    send_coin_amount = Column(Float)
    send_fee = Column(Float)
    receive_coin_amount = Column(Float)
    final_coin_amount = Column(Float)
    backward_fee = Column(Float)
    profit = Column(Float)
