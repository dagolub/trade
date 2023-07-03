from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.translate import _

router = APIRouter()


@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve transaction.
    """
    transactions = crud.transaction.get_multi(db, skip=skip, limit=limit)
    return transactions


@router.post("/", response_model=schemas.Transaction)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.TransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new transaction.
    """

    transaction = crud.transaction.create(db=db, obj_in=transaction_in)

    return transaction


@router.get("/{id}", response_model=schemas.Transaction)
def read_transaction(
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a transaction.
    """
    transaction = crud.transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(
            status_code=400, detail=_("Transaction doesn't exists")
        )
    return transaction


@router.put("/{id}", response_model=schemas.Transaction)
def update_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    transaction_in: schemas.TransactionUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a transaction.
    """
    transaction = crud.transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(
            status_code=404,
            detail=_("Transaction doesn't exists"),
        )
    transaction = crud.transaction.update(db=db, db_obj=transaction, obj_in=transaction_in)
    return transaction


@router.delete("/{id}", response_model=schemas.Transaction)
def delete_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an transaction.
    """
    transaction = crud.transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail=_("Transaction doesn't exists"))

    transaction = crud.transaction.remove(db=db, id=id)
    return transaction