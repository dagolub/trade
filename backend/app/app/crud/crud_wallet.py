from app.crud.base import CRUDBase
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate,  WalletUpdate


class CRUDWallet(CRUDBase[Wallet, WalletCreate, WalletUpdate]):

    async def get_by_deposit(self, db, deposit_id):
        wallet = await db["wallet"].find_one({"deposit_id": deposit_id})  # type: ignore
        if wallet:
            wallet["id"] = str(wallet["_id"])
            return wallet
        else:
            return None

wallet = CRUDWallet(Wallet)
