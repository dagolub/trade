from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from starlette.responses import JSONResponse
import traceback

router = APIRouter()


@router.get("/count")
async def count(
    database: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.withdraw.count(db=database, owner_id=owner_id, search=_search)


@router.get("/", response_model=List[schemas.Withdraw])
async def read_withdraws(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve withdraw.
    """
    _search = _get_search(q)
    withdraws = await crud.withdraw.get_multi(
        db, skip=skip, limit=limit, search=_search
    )
    return withdraws


@router.post("/", response_model=schemas.Withdraw)
async def create_withdraw(
    *,
    db: Session = Depends(deps.get_db),
    withdraw_in: schemas.WithdrawBaseCreated,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new withdraw.
    """
    try:
        withdraw = await crud.withdraw.create(
            db=db, obj_in=withdraw_in, current_user=current_user
        )
    except ValueError as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": e.args[0]},
        )
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
    Delete withdraw.
    """
    withdraw = await crud.withdraw.get(db=db, entity_id=id)
    if not withdraw:
        raise HTTPException(status_code=404, detail="Withdraw doesn't exists")

    withdraw = await crud.withdraw.remove(db=db, entity_id=id)
    return withdraw


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"sum": {"$regex": str(q)}},
                {"to": {"$regex": str(q)}},
                {"status": {"$regex": str(q)}},
            ]
        }
    return search
