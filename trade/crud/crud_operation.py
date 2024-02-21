from trade.crud.base import CRUDBase
from trade.models.operation import Operation
from trade.schemas.operation import OperationCreate, OperationUpdate


class CRUDOperation(CRUDBase[Operation, OperationCreate, OperationUpdate]):
    pass


operation = CRUDOperation(Operation)
