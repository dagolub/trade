from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.db.session import database as db

router = APIRouter()


@router.get("/all", response_model=schemas.Setting)
async def read_setting(
    current_user: models.User = Depends(deps.get_current_active_user),
    mongo_db: Session = Depends(deps.get_db),
) -> Any:
    setting = await crud.setting.get_multi(db=mongo_db)
    if not setting:
        raise HTTPException(status_code=400, detail="Settings doesn't exists")
    return setting[0]


@router.put("/all", response_model=schemas.Setting)
async def update_setting(
    setting_in: schemas.SettingUpdate,
    mongo_db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a deposit.
    """
    setting = await crud.setting.get_multi(db=db)
    if not setting:
        await crud.setting.create(db=db, obj_in={"data": ""})
    setting = await crud.setting.update(  # type: ignore
        db=mongo_db, db_obj=setting[0], obj_in=setting_in  # type: ignore
    )
    return setting
