import random
import string
from app.crud.base import CRUDBase
from app import crud
from app.models.deposit import Deposit
from app.schemas.deposit import DepositCreate, DepositUpdate
from typing import TypeVar, Optional
from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.services.exchanger import Exchanger
from app.schemas.wallet import WalletCreate
from app.tasks.incoming import incoming_transactions

ModelType = TypeVar("ModelType", bound=Base)


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_string_passphrase(length):
    letters = (
        "1234567890" + string.ascii_uppercase + string.ascii_lowercase + "!@#$%^&*()"
    )
    return "".join(random.choice(letters) for i in range(length))


class CRUDDeposit(CRUDBase[Deposit, DepositCreate, DepositUpdate]):
    async def get_by_wallet(self, db, wallet):
        wallet = await db["deposits"].find_one({"wallet": wallet})  # type: ignore
        if wallet:
            wallet["id"] = str(wallet["_id"])
            return wallet
        else:
            return None

    async def get_by_status(self, db, status):
        result = []
        async for wallet in db["deposits"].find({"status": status}):
            wallet["id"] = str(wallet["_id"])
            result.append(wallet)
        return result

    async def create(
        self, db: Session, obj_in: dict, owner=None
    ) -> Optional[ModelType]:
        exchanger = Exchanger()
        okx = exchanger.get("OKX")
        if not okx:
            raise ValueError("Exchanger 'OKX' is not available.")

        sub_account = owner["full_name"] + generate_random_string(5)
        wallet = okx.get_address(sub_account, obj_in.currency, obj_in.chain)

        if not getattr(obj_in, "sum") or not getattr(obj_in, "currency"):
            raise ValueError("'sum' or 'currency' is missing in the input.")

        if not getattr(obj_in, "type"):
            deposit_type = self._get_type()
        else:
            deposit_type = obj_in.type

        passphrase = generate_random_string_passphrase(16)
        sub = okx.create_sub_account_api_key(
            sub_account, sub_account + "Label", passphrase
        )
        deposit_sum = okx.frac_to_int(obj_in.sum, obj_in.currency.lower())
        if "data" in sub and len(sub["data"]) > 0 and len(sub["data"][0]) > 0:
            obj_in = {
                "owner_id": owner["id"],
                "wallet": wallet,
                "type": deposit_type,
                "sum": str(deposit_sum),
                "currency": obj_in.currency,
                "chain": obj_in.chain,
                "status": "waiting",
                "callback": obj_in.callback,
                "callback_response": "",
                "sub_account": sub_account,
                "sub_account_label": sub_account + "Label",
                "sub_account_api_key": sub["data"][0]["apiKey"],
                "sub_account_secret_key": sub["data"][0]["secretKey"],
                "sub_account_passphrase": passphrase,
            }

            current_deposit = await super().create(db=db, obj_in=obj_in)
            await crud.wallet.create(
                db=db,
                obj_in=WalletCreate(
                    owner_id=owner["id"],
                    deposit_id=current_deposit["id"],
                    wallet=wallet,
                    type=deposit_type,
                ),
            )

            return current_deposit
        else:
            raise ValueError("OKX not available")

    def _get_type(self):
        return "OKX"


deposit = CRUDDeposit(Deposit)
