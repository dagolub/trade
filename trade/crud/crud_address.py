from trade.crud.base import CRUDBase
from trade.models.address import Address
from trade.schemas.address import AddressCreate, AddressUpdate


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    pass


address = CRUDAddress(Address)
