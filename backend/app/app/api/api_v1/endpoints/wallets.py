from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/count")
async def count(db: Session = Depends(deps.get_db)) -> int:
    return await crud.wallet.count(db=db)


@router.get("/", response_model=List[schemas.Wallet])
async def read_wallets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve wallet.
    """
    wallets = await crud.wallet.get_multi(db, skip=skip, limit=limit)
    return wallets


@router.post("/", response_model=schemas.Wallet)
async def create_wallet(
    *,
    db: Session = Depends(deps.get_db),
    wallet_in: schemas.WalletCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new wallet.
    """

    wallet = await crud.wallet.create(db=db, obj_in=wallet_in)

    return wallet


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


@router.put("/{id}", response_model=schemas.Wallet)
async def update_wallet(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    wallet_in: schemas.WalletUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a wallet.
    """
    wallet = await crud.wallet.get(db=db, entity_id=id)
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet doesn't exists",
        )
    wallet = await crud.wallet.update(db=db, db_obj=wallet, obj_in=wallet_in)
    return wallet


@router.delete("/{entity_id}", response_model=schemas.Wallet)
async def delete_wallet(
    *,
    db: Session = Depends(deps.get_db),
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an wallet.
    """
    wallet = await crud.wallet.get(db=db, entity_id=entity_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet doesn't exists")

    return await crud.wallet.remove(db=db, entity_id=entity_id)
