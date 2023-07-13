from app.crud.base import CRUDBase
from app.models.deposit import Deposit
from app.schemas.deposit import DepositCreate,  DepositUpdate


class CRUDDeposit(CRUDBase[Deposit, DepositCreate, DepositUpdate]):
    pass


deposit = CRUDDeposit(Deposit)