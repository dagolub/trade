from typing import Dict

import pytest  # type: ignore
from fastapi.testclient import TestClient
from jose import jwt  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import crud
from app.api.deps import get_db
from app.core import security
from app.core.config import settings
from app.main import app
from app.schemas.withdraw import WithdrawCreate
from app.tests.utils import withdraw
from app.tests.utils.db import fake_db

app.dependency_overrides[get_db] = fake_db

# test read
# test create
# test get by id
# test update by id
# test delete by id


@pytest.mark.asyncio
async def test_get_withdraw(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    payload = {}
    for field in {
        "owner_id": "owner_id: Optional[str] = None",
        "to": "to: Optional[str] = None",
        "sum": "sum: Optional[int] = None",
        "created": "created: Optional[datetime.date] = None",
    }:
        value = False
        if "str" in field[1]:
            value = "Some string"
        if "int" in field[1]:
            value = 1111
        payload.setdefault(field[0], value)
    entity = withdraw.create_withdraw(db, payload)
    #  withdraw = await crud.withdraw.get_by_email(db, email=settings.FIRST_SUPERUSER)  # type: ignore
    response = client.get(
        f"{settings.API_V1_STR}/withdraws/{['id']}",  # type: ignore
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
