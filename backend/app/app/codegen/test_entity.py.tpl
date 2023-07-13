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
from app.schemas.{{ entity_lower }} import {{ entity }}Create
from app.tests.utils.db import fake_db
from app.tests.utils import {{ entity_lower }}

app.dependency_overrides[get_db] = fake_db

# test read
# test create
# test get by id
# test update by id
# test delete by id

@pytest.mark.asyncio
async def test_get_{{ entity_lower }}(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    payload = {}
    for field in {{ schema_fields }}:
        value = False
        if 'str' in field[1]:
            value = "Some string"
        if 'int' in field[1]:
            value = 1111
        payload.setdefault(field[0], value)
    entity = {{ entity_lower}}.create_{{entity_lower }}(db, payload)
    #  {{ entity_lower }} = await crud.{{ entity_lower }}.get_by_email(db, email=settings.FIRST_SUPERUSER)  # type: ignore
    response = client.get(
        f"{settings.API_V1_STR}/{{ entity_lower }}s/{['id']}",  # type: ignore
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
