from app import crud
from app.db.session import database as db
from app.schemas.transaction import TransactionCreate


async def incoming_transactions():
    return await crud.transaction.create(
        db=db,
        obj_in=TransactionCreate(
            owner_id=1, from_wallet=1, to_wallet=1, tx=1, amount=1, currency=1, type=1
        ),
    )
