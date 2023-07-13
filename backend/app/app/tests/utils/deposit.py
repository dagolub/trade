from app.crud import crud_deposit as crud

async def create_deposit(db, deposit):
    return await crud.deposit.create(db=db, obj_in=deposit)