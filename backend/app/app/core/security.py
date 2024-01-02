from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt  # type: ignore
from app.core.config import settings
import hashlib
from app.db.session import database as db
from app import crud

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None  # type: ignore
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashlib.md5(plain_password.encode("utf-8")).hexdigest() == hashed_password


def get_password_hash(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


async def validate_token(token: str, type: str):
    apikey = await crud.apikey.get_by_apikey(db=db, token=token)
    if not apikey:
        raise ValueError("Key not found")
    if type not in apikey:
        raise ValueError("You do not have " + type)
    if not apikey[type]:
        raise ValueError("This key not for " + type)


async def start_request(r):
    pass


async def end_request(id, result):
    pass
