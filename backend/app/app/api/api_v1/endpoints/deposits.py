import io
from typing import Any, List
import traceback
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, StreamingResponse
from app.services.client import OKX
from app import crud, models, schemas
from app.api import deps
from app.core.security import validate_token, start_request, end_request
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
import xlwt
from datetime import datetime
import os


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
    return await crud.deposit.count(db=database, owner_id=owner_id, search=_search)


@router.get("/currencies", response_model=[])
async def currencies():
    return ["BTC", "LTC", "USDT", "ETH", "USDC", "XRP", "MATIC", "SOL", "TRX", "TON"]


@router.get("/chains", response_model=[])
async def chains():
    return ["BTC", "LTC", "ERC20", "TRC20", "PLG", "ETH"]


@router.get("/", response_model=List[schemas.Deposit])
async def read_deposits(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    id = await start_request(request)
    search = _get_search(q)
    if current_user["is_superuser"]:
        deposits = await crud.deposit.get_multi(
            db, skip=skip, limit=limit, search=search
        )
    else:
        deposits = await crud.deposit.get_multi_by_owner(
            db, owner_id=current_user["id"], skip=skip, limit=limit, search=search
        )
    result = []
    for deposit in deposits:
        deposit = _deposit(deposit)
        result.append(deposit)
    await end_request(id, result)
    return result


@router.post("/", response_model=schemas.Deposit)
async def create_deposit(
    deposit_in: schemas.DepositBaseCreate,
    token: str = Depends(reusable_oauth2),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Currency: \n
        BTC
        USDT
        USDT
        USDT
        ETH
        USDC
        USDC
        USDC
    Chain: \n
        BTC -> (OKX) BTC-Bitcoin
        LTC -> (OKX) LTC-Litecoin
        ETH -> (OKX) USDT-ERC20
        TRX -> (OKX) USDT-TRC20
        PLG -> (OKX) USDT-Polygon
        ETH -> (OKX) ETH-ERC20"
        ETH -> (OKX) USDC-ERC20
        TRX -> (OKX) USDC-TRC20
        PLG -> (OKX) USDC-Polygon
    """
    try:
        # await validate_token(token, "deposit")
        return _deposit(
            await crud.deposit.create(db=db, obj_in=deposit_in, owner=current_user)  # type: ignore
        )
    except ValueError as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": e.args[0]},
        )


@router.get("/{entity_id}", response_model=schemas.Deposit)
async def read_deposit(
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    deposit = await crud.deposit.get(db=db, entity_id=entity_id)
    if not _deposit:
        raise HTTPException(status_code=400, detail="Deposit doesn't exists")
    deposit = _deposit(deposit)

    return deposit


@router.delete("/{entity_id}", response_model=schemas.Deposit)
async def delete_deposit(
    *,
    db: Session = Depends(deps.get_db),
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    deposit = await crud.deposit.get(db=db, entity_id=entity_id)

    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit doesn't exists")

    wallet = await crud.wallet.get_by_deposit(db=db, deposit_id=deposit["id"])  # type: ignore
    if wallet:
        await crud.wallet.remove(db=db, entity_id=wallet["id"])

    transaction = await crud.transaction.get_by_deposit(db=db, deposit_id=deposit["id"])
    if transaction:
        await crud.transaction.remove(db=db, entity_id=transaction["id"])

    transaction = await crud.transaction.get_by_deposit(db=db, deposit_id=deposit["id"])
    if transaction:
        await crud.transaction.remove(db=db, entity_id=transaction["id"])

    transaction = await crud.transaction.get_by_deposit(db=db, deposit_id=deposit["id"])
    if transaction:
        await crud.transaction.remove(db=db, entity_id=transaction["id"])

    callback = await crud.callback.get_by_deposit(db=db, deposit_id=deposit["id"])  # type: ignore
    if callback:
        await crud.callback.remove(db=db, entity_id=callback["id"])

    return await crud.deposit.remove(db=db, entity_id=entity_id)


@router.post("/export")
async def export(
    response: Response,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if not os.path.exists("export"):
        os.makedirs("export")
    file = f"export/deposit-{datetime.now()}.xls"
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Deposits")
    okx = OKX()
    sheet.write(0, 0, "Email")
    sheet.write(0, 1, "Wallet")
    sheet.write(0, 2, "Sum")
    sheet.write(0, 3, "Paid")
    sheet.write(0, 4, "Fee")
    sheet.write(0, 5, "Currency")
    sheet.write(0, 6, "Chain")
    sheet.write(0, 7, "Status")
    sheet.write(0, 8, "Created")

    if current_user["is_superuser"]:
        deposits = await crud.deposit.get_multi(db=db, skip=0, limit=10000000)
    else:
        deposits = await crud.deposit.get_multi_by_owner(
            db=db, owner_id=current_user["id"], skip=0, limit=10000000
        )
    i = 1
    for deposit in deposits:
        cols = {
            "owner_id": 0,
            "wallet": 1,
            "sum": 2,
            "paid": 3,
            "fee": 4,
            "currency": 5,
            "chain": 6,
            "status": 7,
            "created": 8,
        }
        for j, col in enumerate(deposit):
            if col in cols:
                if col == "owner_id":
                    user = await crud.user.get(db=db, entity_id=deposit[col])
                    if user:
                        cell = user["email"]
                    else:
                        print(user, deposit[col])
                elif col == "created":
                    a = str(deposit[col]).split(".")[0].split(" ")
                    cell = a[1] + " " + a[0]
                elif col == "sum":
                    cell = okx.integer_to_fractional(
                        deposit["sum"], deposit["currency"]
                    )
                elif col == "paid":
                    cell = okx.integer_to_fractional(
                        deposit["paid"], deposit["currency"]
                    )
                elif col == "fee":
                    cell = okx.integer_to_fractional(
                        deposit["fee"], deposit["currency"]
                    )
                else:
                    cell = str(deposit[col])
                sheet.write(i, cols[col], cell)
        i = i + 1

    book.save(file)

    file_content = io.BytesIO(read_binary_file(file))
    return StreamingResponse(file_content, media_type="application/octet-stream")


def read_binary_file(file: str):
    f = open(file, "rb")
    return f.read()


def _deposit(deposit):
    okx = OKX()
    if not okx:
        raise ValueError("Exchanger 'OKX' is not available in parse deposit")
    result = {}
    if deposit is None:
        raise ValueError("Wrong deposit")
    result.setdefault("id", deposit["id"])
    if "owner_id" in deposit:
        result.setdefault("owner_id", deposit["owner_id"])
    else:
        result.setdefault("owner_id", "")
    result.setdefault("wallet", deposit["wallet"])
    result.setdefault("type", deposit["type"])
    if "exchange" in deposit:
        result.setdefault("exchange", deposit["exchange"])
    else:
        result.setdefault("exchange", "")
    result.setdefault("status", deposit["status"])
    if "paid" in deposit:
        result.setdefault(
            "paid",
            okx.integer_to_fractional(deposit["paid"], deposit["currency"]),
        )
    else:
        result.setdefault("paid", 0)
    result.setdefault("callback", deposit["callback"])
    result.setdefault("callback_response", deposit["callback_response"])
    result.setdefault(
        "sum", okx.integer_to_fractional(deposit["sum"], deposit["currency"])
    )
    result.setdefault("currency", deposit["currency"])
    result.setdefault("chain", deposit["chain"])
    if "fee" in deposit:
        result.setdefault(
            "fee",
            okx.integer_to_fractional(deposit["fee"], deposit["currency"]),
        )
    else:
        result.setdefault("fee", 0)
    result.setdefault("created", str(deposit["created"]))
    return result


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"sum": {"$regex": str(q)}},
                {"currency": {"$regex": str(q)}},
                {"status": {"$regex": str(q)}},
                {"wallet": {"$regex": str(q)}},
                {"chain": {"$regex": str(q)}},
            ]
        }
    return search
