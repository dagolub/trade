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
from app.schemas.wallet import WalletCreate
from app.tests.utils.db import fake_db


app.dependency_overrides[get_db] = fake_db

# test read
# test create
# test get by id
# test update by id
# test delete by id

@pytest.mark.asyncio
async def test_get_wallet(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    #  wallet = await crud.wallet.get_by_email(db, email=settings.FIRST_SUPERUSER)  # type: ignore
    response = client.get(
        f"{settings.API_V1_STR}/wallets/{['id']}",  # type: ignore
        headers=superuser_token_headers,
    )
    assert response.status_code == 200