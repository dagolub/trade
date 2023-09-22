from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/count")
async def count(
    db: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.deposit.count(db=db, owner_id=owner_id, search=_search)


@router.get("/", response_model=List[schemas.Wallet])
async def read_wallets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve wallet.
    """
    search = _get_search(q)
    if current_user["is_superuser"]:
        wallets = await crud.wallet.get_multi(db, skip=skip, limit=limit, search=search)
    else:
        wallets = await crud.wallet.get_multi_by_owner(
            db, owner_id=current_user["id"], skip=skip, limit=limit, search=search
        )
    return wallets


@router.get("/{id}", response_model=schemas.Wallet)
async def read_wallet(
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a wallet.
    """
    wallet = await crud.wallet.get(db=db, entity_id=id)
    if not wallet:
        raise HTTPException(status_code=400, detail="Wallet doesn't exists")
    return wallet


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"wallet": {"$regex": str(q)}},
                {"type": {"$regex": str(q)}},
            ]
        }
    return search
