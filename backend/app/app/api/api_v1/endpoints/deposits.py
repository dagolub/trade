from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.translate import _

router = APIRouter()


@router.get("/", response_model=List[schemas.Deposit])
def read_deposits(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve deposit.
    """
    deposits = crud.deposit.get_multi(db, skip=skip, limit=limit)
    return deposits


@router.post("/", response_model=schemas.Deposit)
def create_deposit(
    *,
    db: Session = Depends(deps.get_db),
    deposit_in: schemas.DepositCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new deposit.
    """

    deposit = crud.deposit.create(db=db, obj_in=deposit_in)

    return deposit


@router.get("/{id}", response_model=schemas.Deposit)
def read_deposit(
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a deposit.
    """
    deposit = crud.deposit.get(db=db, id=id)
    if not deposit:
        raise HTTPException(
            status_code=400, detail=_("Deposit doesn't exists")
        )
    return deposit


@router.put("/{id}", response_model=schemas.Deposit)
def update_deposit(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    deposit_in: schemas.DepositUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a deposit.
    """
    deposit = crud.deposit.get(db=db, id=id)
    if not deposit:
        raise HTTPException(
            status_code=404,
            detail=_("Deposit doesn't exists"),
        )
    deposit = crud.deposit.update(db=db, db_obj=deposit, obj_in=deposit_in)
    return deposit


@router.delete("/{id}", response_model=schemas.Deposit)
def delete_deposit(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an deposit.
    """
    deposit = crud.deposit.get(db=db, id=id)
    if not deposit:
        raise HTTPException(status_code=404, detail=_("Deposit doesn't exists"))

    deposit = crud.deposit.remove(db=db, id=id)
    return deposit