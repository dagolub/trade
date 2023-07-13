from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.get("/", response_model=List[schemas.Wallet])
def read_wallets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve wallet.
    """
    wallets = crud.wallet.get_multi(db, skip=skip, limit=limit)
    return wallets


@router.post("/", response_model=schemas.Wallet)
def create_wallet(
    *,
    db: Session = Depends(deps.get_db),
    wallet_in: schemas.WalletCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new wallet.
    """

    wallet = crud.wallet.create(db=db, obj_in=wallet_in)

    return wallet


@router.get("/{id}", response_model=schemas.Wallet)
def read_wallet(
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a wallet.
    """
    wallet = crud.wallet.get(db=db, id=id)
    if not wallet:
        raise HTTPException(
            status_code=400, detail=_("Wallet doesn't exists")
        )
    return wallet


@router.put("/{id}", response_model=schemas.Wallet)
def update_wallet(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    wallet_in: schemas.WalletUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a wallet.
    """
    wallet = crud.wallet.get(db=db, id=id)
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail=_("Wallet doesn't exists"),
        )
    wallet = crud.wallet.update(db=db, db_obj=wallet, obj_in=wallet_in)
    return wallet


@router.delete("/{id}", response_model=schemas.Wallet)
def delete_wallet(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an wallet.
    """
    wallet = crud.wallet.get(db=db, id=id)
    if not wallet:
        raise HTTPException(status_code=404, detail=_("Wallet doesn't exists"))

    wallet = crud.wallet.remove(db=db, id=id)
    return wallet