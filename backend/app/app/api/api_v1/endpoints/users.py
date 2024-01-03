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


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


@router.get("/count")
async def count(
    db: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.user.count(db=db, owner_id=owner_id, search=_search)


# @router.get("/get_otp/{email}")
# async def get_otp(
#     email: str = None, current_user: models.User = Depends(deps.get_current_active_user)  # type: ignore
# ):  # type: ignore
#     url = pyotp.totp.TOTP("JBSWY3DPEHPK3PXP").provisioning_uri(
#         name=email, issuer_name="RPAY"
#     )
#
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#
#     # Add the OTP URI data to the QR code
#     qr.add_data(url)
#     qr.make(fit=True)
#
#     # Create an image from the QR code instance
#     qr_image = qr.make_image(fill_color="black", back_color="white")
#
#     random_string = generate_random_string(10)
#     image_url = f"images/{random_string}.png"
#
#     # Save the QR code image
#     qr_image.save(image_url)
#
#     return image_url


@router.get("/apikeys")
async def get_api_keys(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    data = await crud.apikey.get_multi_by_owner(db, owner_id=current_user["id"])
    result = []
    for item in data:
        result.append(
            {"id": item["id"], "owner_id": item["owner_id"], "apikey": item["apikey"]}
        )
    return result


@router.put("/apikeys")
async def get_api_keys(
    obj: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    obj_in = {}
    obj_in["owner_id"] = current_user["id"]
    access_token_expires = timedelta(minutes=(60 * 24 * 365))
    obj_in["apikey"] = security.create_access_token(
        current_user["id"], expires_delta=access_token_expires  # type: ignore
    )
    if hasattr(obj, "deposit"):
        obj_in["deposit"] = True
    else:
        obj_in["deposit"] = False

    if hasattr(obj, "withdraw"):
        obj_in["withdraw"] = True
    else:
        obj_in["withdraw"] = False

    if hasattr(obj, "ips"):
        obj_in["ips"] = obj.ips

    if hasattr(obj, "id"):
        result = await crud.apikey.update(db=db, db_obj={"id": obj.id}, obj_in=obj_in)
    else:
        result = await crud.apikey.create(db, obj_in=obj_in)
    return {"id": result["id"], "owner_id": result["owner_id"]}


@router.get("/apikeys/{id}")
async def get_api_keys(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    result = await crud.apikey.get(db=db, entity_id=id)
    if "ips" not in result:
        result["ips"] = ""
    if "deposit" not in result:
        result["deposit"] = False
    if "withdraw" not in result:
        result["withdraw"] = False
    return {
        "deposit": result["deposit"],
        "withdraw": result["withdraw"],
        "ips": result["ips"],
    }


@router.delete("/apikeys/{id}")
async def get_api_keys(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    result = await crud.apikey.remove(db=db, entity_id=id)
    return result


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


@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Retrieve users.
    """
    _search = _get_search(q)
    users = await crud.user.get_multi(db, skip=skip, limit=limit, search=_search)  # type: ignore
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user = await crud.user.create(db, obj_in=jsonable_encoder(user_in))
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.get("/{entity_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.user.get(db, entity_id=entity_id)  # type: ignore
    if user["email"] == current_user["email"]:  # type: ignore
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{entity_id}", response_model=schemas.User)
async def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),  # noqa
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get(db, entity_id=entity_id)  # type: ignore
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await crud.user.update(db, db_obj=user, obj_in=entity_id)  # type: ignore
    return user


@router.delete("/{entity_id}", response_model=schemas.User)
async def delete_deposit(
    entity_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    user = await crud.user.get(db=db, entity_id=entity_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exists")

    return await crud.user.remove(db=db, entity_id=entity_id)


@router.post("/open", response_model=schemas.User)
async def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
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
    user_in.autotransfer = False
    user = await crud.user.create(db, obj_in=user_in)
    return user
