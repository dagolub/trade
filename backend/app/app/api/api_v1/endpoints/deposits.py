from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import crud, models, schemas
from app.api import deps
from app.cron.callback import get_callback
from app.db.session import database as db
from app.services.exchanger import Exchanger

router = APIRouter()


@router.get("/count")
async def count(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.deposit.count(db=db, owner_id=owner_id)


@router.get("/", response_model=List[schemas.Deposit])
async def read_deposits(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    if not okx:
        raise ValueError("Exchanger 'OKX' is not available.")

    if current_user["is_superuser"]:
        deposits = await crud.deposit.get_multi(db, skip=skip, limit=limit)
    else:
        deposits = await crud.deposit.get_multi_by_owner(
            db, owner_id=current_user["id"], skip=skip, limit=limit
        )
    result = []
    for deposit in deposits:
        deposit = _deposit(deposit)
        result.append(deposit)
    return result


@router.post("/", response_model=schemas.Deposit)
async def create_deposit(
    *,
    db: Session = Depends(deps.get_db),
    deposit_in: schemas.DepositCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new deposit.
    """
    try:
        return _deposit(
            await crud.deposit.create(db=db, obj_in=deposit_in, owner=current_user)  # type: ignore
        )
    except ValueError as e:
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
    """
    Get a deposit.
    """
    deposit = _deposit(await crud.deposit.get(db=db, entity_id=entity_id))
    if not deposit:
        raise HTTPException(status_code=400, detail="Deposit doesn't exists")
    return deposit


@router.put("/{entity_id}", response_model=schemas.Deposit)
async def update_deposit(
    *,
    db: Session = Depends(deps.get_db),
    entity_id: str,
    deposit_in: schemas.DepositUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a deposit.
    """
    deposit = await crud.deposit.get(db=db, entity_id=entity_id)
    if not deposit:
        raise HTTPException(
            status_code=404,
            detail="Deposit doesn't exists",
        )
    deposit = await crud.deposit.update(db=db, db_obj=deposit, obj_in=deposit_in)  # type: ignore
    return deposit


@router.delete("/{entity_id}", response_model=schemas.Deposit)
async def delete_deposit(
    *,
    db: Session = Depends(deps.get_db),
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an deposit.
    """
    deposit = await crud.deposit.get(db=db, entity_id=entity_id)
    wallet = await crud.wallet.get_by_deposit(db=db, deposit_id=deposit["id"])  # type: ignore
    await crud.wallet.remove(db=db, entity_id=wallet["id"])
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit doesn't exists")

    return await crud.deposit.remove(db=db, entity_id=entity_id)


@router.get("/callback/{entity_id}")
async def callback(entity_id: str):
    original_deposit = await crud.deposit.get(db=db, entity_id=entity_id)
    deposit = _deposit(original_deposit)
    response, status_code = get_callback(deposit["callback"], deposit)
    await crud.deposit.update(
        db=db, db_obj=original_deposit, obj_in={"callback_response": response}  # type: ignore
    )
    return response


def _deposit(deposit):
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    if not okx:
        raise ValueError("Exchanger 'OKX' is not available in parse deposit")
    result = {}
    result.setdefault("id", deposit["id"])
    result.setdefault("wallet", deposit["wallet"])
    result.setdefault("type", deposit["type"])
    result.setdefault("status", deposit["status"])
    result.setdefault("callback", deposit["callback"])
    result.setdefault("callback_response", deposit["callback_response"])
    result.setdefault("sum", okx.int_to_frac(deposit["sum"], deposit["currency"]))
    result.setdefault("currency", deposit["currency"])
    result.setdefault("chain", deposit["chain"])
    result.setdefault("created", str(deposit["created"]))
    return result
