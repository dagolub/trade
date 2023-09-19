from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/count")
async def count(db: Session = Depends(deps.get_db)) -> int:
    return await crud.withdraw.count(db=db)


@router.get("/", response_model=List[schemas.Withdraw])
async def read_withdraws(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve withdraw.
    """
    withdraws = await crud.withdraw.get_multi(db, skip=skip, limit=limit)
    return withdraws


@router.post("/", response_model=schemas.Withdraw)
async def create_withdraw(
    *,
    db: Session = Depends(deps.get_db),
    withdraw_in: schemas.WithdrawCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new withdraw.
    """

    withdraw = await crud.withdraw.create(db=db, obj_in=withdraw_in)

    return withdraw


@router.get("/{id}", response_model=schemas.Withdraw)
async def read_withdraw(
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a withdraw.
    """
    withdraw = await crud.withdraw.get(db=db, entity_id=id)
    if not withdraw:
        raise HTTPException(status_code=400, detail="Withdraw doesn't exists")
    return withdraw


@router.delete("/{id}", response_model=schemas.Withdraw)
async def delete_withdraw(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an withdraw.
    """
    withdraw = await crud.withdraw.get(db=db, id=id)
    if not withdraw:
        raise HTTPException(status_code=404, detail="Withdraw doesn't exists")

    withdraw = await crud.withdraw.remove(db=db, id=id)
    return withdraw
