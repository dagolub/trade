from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app.services.exchanger import Exchanger
from app import crud, models, schemas
from app.api import deps
from app.cron.callback import get_callback
from app.db.session import database as db

router = APIRouter()


@router.get("/all", response_model=schemas.Setting)
async def read_deposit(
    current_user: models.User = Depends(deps.get_current_active_user),
    mongo_db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a deposit.
    """
    setting = await crud.setting.get_multi(db=mongo_db)
    if not setting:
        raise HTTPException(status_code=400, detail="Settings doesn't exists")
    return setting[0]


@router.put("/all", response_model=schemas.Setting)
async def update_deposit(
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
    setting = await crud.setting.update(
        db=mongo_db, db_obj=setting[0], obj_in=setting_in
    )
    return setting
