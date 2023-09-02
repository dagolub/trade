import random
import string
from datetime import datetime
from typing import Optional, TypeVar

from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.deposit import Deposit
from app.schemas.deposit import DepositCreate, DepositUpdate
from app.services.exchanger import Exchanger

ModelType = TypeVar("ModelType", bound=Base)


def generate_random_ints(length):
    letters = "01234567890"
    return "".join(random.choice(letters) for i in range(length))


def generate_random_small(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_big(length):
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_string_passphrase(length):
    letters = "!@#$%^&*()[]/?;':.,<>|-_=+`~"
    random_int = generate_random_ints(4)
    random_string = generate_random_small(2) + generate_random_big(2) + random_int
    return random_string.join(random.choice(letters) for i in range(length - 8))


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

    async def create(  # type: ignore
        self, db: Session, obj_in: dict, owner=None
    ) -> Optional[ModelType]:
        exchanger = Exchanger()
        okx = exchanger.get("OKX")
        if not okx:
            raise ValueError("OKX is not available in crud_deposit create")

        sub_account = (
            owner["full_name"] + generate_random_small(3) + generate_random_big(3)
        )
        wallet = okx.get_address(sub_account, obj_in.currency, obj_in.chain)  # type: ignore

        if not getattr(obj_in, "sum") or not getattr(obj_in, "currency"):
            raise ValueError("'sum' or 'currency' is missing in the input.")

        if not getattr(obj_in, "chain") or not getattr(obj_in, "currency"):
            raise ValueError("Chain is empty")

        if not getattr(obj_in, "type"):
            deposit_type = self._get_type()
        else:
            deposit_type = obj_in.type  # type: ignore

        passphrase = generate_random_string_passphrase(12)
        sub = okx.create_sub_account_api_key(
            sub_account, sub_account + "Label", passphrase
        )
        deposit_sum = okx.frac_to_int(obj_in.sum, obj_in.currency.lower())  # type: ignore
        if "data" in sub and len(sub["data"]) > 0 and len(sub["data"][0]) > 0:
            obj_in = {
                "owner_id": owner["id"],
                "wallet": wallet,
                "type": deposit_type,
                "sum": str(deposit_sum),
                "currency": obj_in.currency,  # type: ignore
                "chain": obj_in.chain,  # type: ignore
                "status": "created",
                "callback": obj_in.callback,  # type: ignore
                "callback_response": "",
                "sub_account": sub_account,
                "sub_account_label": sub_account + "Label",
                "sub_account_api_key": sub["data"][0]["apiKey"],
                "sub_account_secret_key": sub["data"][0]["secretKey"],
                "sub_account_passphrase": passphrase,
                "created": datetime.utcnow(),
            }

            current_deposit = await super().create(db=db, obj_in=obj_in)
            await crud.wallet.create(
                db=db,
                obj_in={  # type: ignore
                    "owner_id": owner["id"],
                    "deposit_id": current_deposit["id"],  # type: ignore
                    "wallet": wallet,
                    "type": deposit_type,
                    "created": datetime.utcnow(),
                },
            )

            return current_deposit  # type: ignore
        else:
            raise ValueError("OKX not available")

    def _get_type(self):
        return "OKX"


deposit = CRUDDeposit(Deposit)
