import random
import string
from datetime import datetime
from typing import Optional, TypeVar
import sentry_sdk
from sqlalchemy.orm import Session
from app import crud
from app.crud.base import CRUDBase
from app.db.base_class import Base
from app.models.deposit import Deposit
from app.schemas.deposit import DepositCreate, DepositUpdate
from app.services.client import OKX
import traceback
from fastapi.encoders import jsonable_encoder

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
        wallet = await db["deposit"].find_one({"wallet": wallet})  # type: ignore
        if wallet:
            wallet["id"] = str(wallet["_id"])
            return wallet
        else:
            return None

    def _get_min_deposit(
        self, currencies: [], currency: str, chain: str, amount: float
    ):
        okx = OKX()
        for c in currencies:
            if str(c["ccy"]) == str(currency):
                _chain = okx.get_currency_chain(currency, chain)
                if c["chain"] == _chain:
                    if "minDep" in c:
                        return c["minDep"]

    async def create(  # noqa: 901
        self, db: Session, obj_in: dict, owner=None
    ) -> Optional[ModelType]:
        try:
            okx = OKX()
            if not okx:
                raise ValueError("OKX is not available in crud_deposit create")
            currencies = okx.get_currencies()

            if obj_in.sum and not hasattr(obj_in, "fee"):
                min_deposit = self._get_min_deposit(
                    currencies["data"],
                    str(obj_in.currency),
                    str(obj_in.chain),
                    float(obj_in.sum),
                )
            else:
                min_deposit = 0
            if obj_in.sum and not hasattr(obj_in, "fee"):
                if float(obj_in.sum) < float(min_deposit):
                    raise ValueError(
                        f"Min deposit in {obj_in.currency} {obj_in.chain} is {min_deposit}"
                    )

            if not obj_in.sub_account:
                sub_account = (
                    owner["full_name"]
                    + generate_random_small(3)
                    + generate_random_big(3)
                )
            else:
                sub_account = obj_in.sub_account

            if hasattr(obj_in, "wallet"):
                wallet = obj_in.wallet
            else:
                wallet = okx.get_address(sub_account, obj_in.currency, obj_in.chain)  # type: ignore

            if obj_in.sum:
                if not getattr(obj_in, "sum") or not getattr(obj_in, "currency"):
                    raise ValueError("'sum' or 'currency' is missing in the input.")

            if not getattr(obj_in, "chain") or not getattr(obj_in, "currency"):
                raise ValueError("Chain is empty")

            if not "type" in dir(obj_in) or not getattr(obj_in, "type"):  # noqa
                deposit_type = self._get_type()
            else:
                deposit_type = obj_in.type  # type: ignore

            if obj_in.sum and not hasattr(obj_in, "fee"):
                deposit_sum = str(okx.fractional_to_integer(obj_in.sum, obj_in.currency.lower()))  # type: ignore
            else:
                deposit_sum = str(0)
            current_deposit = None
            if owner and sub_account:
                user = await crud.user.get(db=db, entity_id=owner["id"])
                if (
                    "commissions" in user
                    and obj_in.currency.lower() in user["commissions"]  # noqa
                ):
                    comm = user["commissions"][obj_in.currency.lower()]["in"]
                else:
                    comm = {"percent": 0, "fixed": 0}
                if obj_in.sum and not hasattr(obj_in, "fee"):
                    fee = okx.fractional_to_integer(
                        float(obj_in.sum) * 0.0100 * float(comm["percent"])
                        + float(comm["fixed"]),  # noqa
                        obj_in.currency.lower(),
                    )
                else:
                    fee = 0

                if hasattr(obj_in, "fee"):
                    fee = obj_in.fee

                if hasattr(obj_in, "fee") and hasattr(obj_in, "sum"):
                    deposit_sum = obj_in.sum
                obj_in = {
                    "owner_id": owner["id"],
                    "wallet": wallet,
                    "type": deposit_type,
                    "sum": deposit_sum,
                    "currency": obj_in.currency,  # type: ignore
                    "chain": obj_in.chain,  # type: ignore
                    "status": obj_in.status if hasattr(obj_in, "status") else "created",
                    "callback": obj_in.callback,  # type: ignore
                    "callback_response": "",
                    "sub_account": sub_account,
                    "fee": fee,
                    "created": datetime.utcnow(),
                }

                current_deposit = await super().create(db=db, obj_in=obj_in)

                if not hasattr(obj_in, "wallet"):
                    await crud.wallet.create(
                        db=db,
                        obj_in={  # type: ignore
                            "deposit_id": current_deposit["id"],  # type: ignore
                            "wallet": wallet,
                            "type": deposit_type,
                            "created": datetime.utcnow(),
                            "owner_id": owner["id"],
                        },
                    )

            return current_deposit  # type: ignore
        except Exception as e:
            sentry_sdk.capture_exception(e)
            traceback.print_exc()

            raise ValueError("Can not create deposit " + str(e.args[0]))

    def _get_type(self):
        return "OKX"


deposit = CRUDDeposit(Deposit)
