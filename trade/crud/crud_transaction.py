from trade.crud.base import CRUDBase
from trade.models.transaction import Transaction
from trade.schemas.transaction import TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    pass


transaction = CRUDTransaction(Transaction)
