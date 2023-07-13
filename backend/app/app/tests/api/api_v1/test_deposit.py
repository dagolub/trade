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
from app.schemas.deposit import DepositCreate
from app.tests.utils.db import fake_db
from app.tests.utils import deposit

app.dependency_overrides[get_db] = fake_db

# test read
# test create
# test get by id
# test update by id
# test delete by id

@pytest.mark.asyncio
async def test_get_deposit(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    payload = {}
    fields = {'owner_id': 'owner_id: Optional[str] = None', 'wallet': 'wallet: Optional[str] = None', 'type': 'type: Optional[str] = None', 'sum': 'sum: Optional[int] = None', 'currency': 'currency: Optional[str] = None'}
    for field in fields:
        value = False
        if 'str' in fields[field]:
            value = "Some string"
        if 'int' in fields[field]:
            value = 1111
        payload.setdefault(field, value)
    entity = await deposit.create_deposit(db, payload)
    #  deposit = await crud.deposit.get_by_email(db, email=settings.FIRST_SUPERUSER)  # type: ignore
    response = client.get(
        f"{settings.API_V1_STR}/deposits/{['id']}",  # type: ignore
        headers=superuser_token_headers,
    )
    assert response.status_code == 200