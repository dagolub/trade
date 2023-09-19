from app.crud.base import CRUDBase
from app.models.withdraw import Withdraw
from app.schemas.withdraw import WithdrawCreate, WithdrawUpdate


class CRUDWithdraw(CRUDBase[Withdraw, WithdrawCreate, WithdrawUpdate]):
    pass


withdraw = CRUDWithdraw(Withdraw)
