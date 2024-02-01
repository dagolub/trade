import random
import string
from typing import Any, List, Optional
import pyotp
import qrcode  # type: ignore
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session  # type: ignore
from datetime import datetime
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email
from app.core import security
from datetime import timedelta


router = APIRouter()


@router.get("/count")
async def count(
    db: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.user.count(db=db, owner_id=owner_id, search=_search)


@router.post("/open", response_model=schemas.User)
async def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    user = await crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user_in.created = datetime.utcnow()
    user_in.is_superuser = False
    user_in.is_active = True
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.post("/", response_model=schemas.User)
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = await crud.user.create(db, obj_in=jsonable_encoder(user_in))
    if user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.get("/me", response_model=schemas.User)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return current_user


@router.put("/{entity_id}", response_model=schemas.User)
async def update_user(
    *,
    db: Session = Depends(deps.get_db),
    entity_id: str,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    user = await crud.user.get(db, entity_id=entity_id)  # type: ignore
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)  # type: ignore
    return user


@router.get("/{entity_id}", response_model=schemas.User)
async def read_user_by_id(
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: Session = Depends(deps.get_db),
) -> Any:
    user = await crud.user.get(db, entity_id=entity_id)  # type: ignore
    if user["email"] == current_user["email"]:  # type: ignore
        return user

    return user


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    _search = _get_search(q)
    users = await crud.user.get_multi(db, skip=skip, limit=limit, search=_search)  # type: ignore
    return users


@router.delete("/{entity_id}", response_model=schemas.User)
async def delete_deposit(
    entity_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    user = await crud.user.get(db=db, entity_id=entity_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exists")

    return await crud.user.remove(db=db, entity_id=entity_id)


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"full_name": {"$regex": str(q)}},
                {"email": {"$regex": str(q)}},
            ]
        }
    return search
