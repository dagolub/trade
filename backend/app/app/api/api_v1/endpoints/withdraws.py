from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from starlette.responses import JSONResponse
import traceback
from app.core.security import validate_token
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
import xlwt
from datetime import datetime
import os
from app.services.client import OKX

router = APIRouter()

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


@router.get("/count")
async def count(
    database: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.withdraw.count(db=database, owner_id=owner_id, search=_search)


@router.get("/", response_model=List[schemas.Withdraw])
async def read_withdraws(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    search = _get_search(q)
    result = []

    if current_user["is_superuser"]:
        withdraws = await crud.withdraw.get_multi(
            db, skip=skip, limit=limit, search=search
        )
    else:
        withdraws = await crud.withdraw.get_multi_by_owner(
            db, owner_id=current_user["id"], skip=skip, limit=limit, search=search
        )

    for w in withdraws:
        result.append(w)
    return result


@router.post("/", response_model=schemas.Withdraw)
async def create_withdraw(
    withdraw_in: schemas.WithdrawBaseCreated,
    token: str = Depends(reusable_oauth2),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    try:
        # await validate_token(token, "withdraw")
        withdraw = await crud.withdraw.create(
            db=db, obj_in=withdraw_in, current_user=current_user
        )
    except ValueError as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": e.args[0]},
        )
    return withdraw


@router.get("/{id}", response_model=schemas.Withdraw)
async def read_withdraw(
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    withdraw = await crud.withdraw.get(db=db, entity_id=id)
    if not withdraw:
        raise HTTPException(status_code=400, detail="Withdraw doesn't exists")
    return withdraw


@router.post("/export")
async def export(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if not os.path.exists("export"):
        os.makedirs("export")
    file = f"export/withdraw-{datetime.now()}.xls"
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Withdraw")
    okx = OKX()
    sheet.write(0, 0, "Email")
    sheet.write(0, 1, "Wallet")
    sheet.write(0, 2, "Sum")
    sheet.write(0, 3, "Fee")
    sheet.write(0, 4, "Currency")
    sheet.write(0, 5, "Chain")
    sheet.write(0, 6, "Status")
    sheet.write(0, 7, "Created")

    if current_user["is_superuser"]:
        deposits = await crud.withdraw.get_multi(db=db, skip=0, limit=10000000)
    else:
        deposits = await crud.withdraw.get_multi_by_owner(
            db=db, owner_id=current_user["id"], skip=0, limit=10000000
        )
    i = 1
    for deposit in deposits:
        cols = {
            "owner_id": 0,
            "to": 1,
            "sum": 2,
            "fee": 3,
            "currency": 4,
            "chain": 5,
            "status": 6,
            "created": 7,
        }
        for j, col in enumerate(deposit):
            if col in cols:
                if col == "owner_id":
                    user = await crud.user.get(db=db, entity_id=deposit[col])
                    cell = user["email"]
                elif col == "created":
                    a = str(deposit[col]).split(".")[0].split(" ")
                    cell = a[1] + " " + a[0]
                else:
                    cell = str(deposit[col])
                sheet.write(i, cols[col], cell)
        i = i + 1

    book.save(file)


@router.delete("/{id}", response_model=schemas.Withdraw)
async def delete_withdraw(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    withdraw = await crud.withdraw.get(db=db, entity_id=id)
    if not withdraw:
        raise HTTPException(status_code=404, detail="Withdraw doesn't exists")

    transaction = await crud.transaction.get_by_withdraw(db=db, withdraw_id=id)
    while transaction:
        await crud.transaction.remove(db=db, entity_id=transaction["id"])
        transaction = await crud.transaction.get_by_withdraw(db=db, withdraw_id=id)

    withdraw = await crud.withdraw.remove(db=db, entity_id=id)
    return withdraw


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"sum": {"$regex": str(q)}},
                {"to": {"$regex": str(q)}},
                {"status": {"$regex": str(q)}},
            ]
        }
    return search
