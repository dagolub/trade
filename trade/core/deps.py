from typing import Generator
from trade.db.session import database as db


def get_db() -> Generator:
    try:
        yield db
    finally:
        db.close()
