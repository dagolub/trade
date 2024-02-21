from trade.crud.base import CRUDBase
from trade.models.customer import Customer
from trade.schemas.customer import CustomerCreate, CustomerUpdate


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):
    pass


customer = CRUDCustomer(Customer)
