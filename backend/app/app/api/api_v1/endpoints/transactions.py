from typing import Any, List

from app import crud, models, schemas
from app.api import deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/count")
async def count(
    database: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.transaction.count(db=database, owner_id=owner_id, search=_search)


@router.get("/", response_model=List[schemas.Transaction])
async def read_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve transaction.
    """
    _search = _get_search(q)
    if current_user["is_superuser"]:
        transactions = await crud.transaction.get_multi(
            db, skip=skip, limit=limit, search=_search
        )
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


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"from_wallet": {"$regex": str(q)}},
                {"to_wallet": {"$regex": str(q)}},
                {"tx": {"$regex": str(q)}},
                {"currency": {"$regex": str(q)}},
                {"amount": {"$regex": str(q)}},
            ]
        }
    return search
