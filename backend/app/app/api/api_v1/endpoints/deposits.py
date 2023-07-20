from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/count")
async def count(db: Session = Depends(deps.get_db)) -> int:
    return await crud.deposit.count(db=db)


@router.get("/", response_model=List[schemas.Deposit])
async def read_deposits(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve deposit.
    """
    deposits = await crud.deposit.get_multi(db, skip=skip, limit=limit)
    return deposits


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

    deposit = await crud.deposit.create(db=db, obj_in=deposit_in)

    return deposit


@router.get("/{id}", response_model=schemas.Deposit)
async def read_deposit(
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a deposit.
    """
    deposit = await crud.deposit.get(db=db, entity_id=id)
    if not deposit:
        raise HTTPException(
            status_code=400, detail="Deposit doesn't exists"
        )
    return deposit


@router.put("/{id}", response_model=schemas.Deposit)
async def update_deposit(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    deposit_in: schemas.DepositUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a deposit.
    """
    deposit = await crud.deposit.get(db=db, entity_id=id)
    if not deposit:
        raise HTTPException(
            status_code=404,
            detail="Deposit doesn't exists",
        )
    deposit = await crud.deposit.update(db=db, db_obj=deposit, obj_in=deposit_in)
    return deposit


@router.delete("/{id}", response_model=schemas.Deposit)
async def delete_deposit(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an deposit.
    """
    deposit = await crud.deposit.get(db=db, id=id)
    if not deposit:
        raise HTTPException(status_code=404, detail="Deposit doesn't exists")

    deposit = await crud.deposit.remove(db=db, id=id)
    return deposit