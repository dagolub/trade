from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/count")
async def count(db: Session = Depends(deps.get_db)) -> int:
    return await crud.transaction.count(db=db)


@router.get("/", response_model=List[schemas.Transaction])
async def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve transaction.
    """
    if current_user["is_superuser"]:
        transactions = await crud.transaction.get_multi(db, skip=skip, limit=limit)
    else:
        transactions = await crud.transaction.get_multi_by_owner(
            db, owner_id=current_user["id"], skip=skip, limit=limit
        )
    return transactions


@router.post("/", response_model=schemas.Transaction)
async def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.TransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new transaction.
    """

    transaction = await crud.transaction.create(db=db, obj_in=transaction_in)  # type: ignore

    return transaction


@router.get("/{id}", response_model=schemas.Transaction)
async def read_transaction(
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a transaction.
    """
    transaction = await crud.transaction.get(db=db, entity_id=id)
    if not transaction:
        raise HTTPException(status_code=400, detail="Transaction doesn't exists")
    return transaction


@router.put("/{id}", response_model=schemas.Transaction)
async def update_transaction(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    transaction_in: schemas.TransactionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a transaction.
    """
    transaction = await crud.transaction.get(db=db, entity_id=id)
    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction doesn't exists",
        )
    transaction = await crud.transaction.update(
        db=db, db_obj=transaction, obj_in=transaction_in  # type: ignore
    )
    return transaction


@router.delete("/{entity_id}", response_model=schemas.Transaction)
async def delete_transaction(
    *,
    db: Session = Depends(deps.get_db),
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an transaction.
    """
    transaction = await crud.transaction.get(db=db, entity_id=entity_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction doesn't exists")

    return await crud.transaction.remove(db=db, entity_id=entity_id)
