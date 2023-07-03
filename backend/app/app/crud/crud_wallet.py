from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate,  WalletUpdate


class CRUDWallet(CRUDBase[Wallet, WalletCreate, WalletUpdate]):
    pass


wallet = CRUDWallet(Wallet)