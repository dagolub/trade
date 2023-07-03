from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.deposit import Deposit
from app.schemas.deposit import DepositCreate,  DepositUpdate


class CRUDDeposit(CRUDBase[Deposit, DepositCreate, DepositUpdate]):
    pass


deposit = CRUDDeposit(Deposit)