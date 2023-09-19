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
