from typing import Any, List
import qrcode  # type: ignore
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings


router = APIRouter()


@router.get("/count")
async def count(
    db: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.folder.count(db=db, owner_id=owner_id, search=_search)


@router.post("/", response_model=schemas.Folder)
async def create_folder(
    folder_in: schemas.FolderCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    if hasattr(folder_in, "folder_id") and folder_in.folder_id != 0:
        folder_id = folder_in.folder_id
    else:
        folder_id = 4
    folder_in = {
        "owner_id": current_user["id"],
        "name": folder_in.name,
        "folder_id": folder_id,
    }
    folder = await crud.folder.create(db=db, obj_in=folder_in)

    return folder


@router.put("/{entity_id}", response_model=schemas.Folder)
async def update_folder(
    entity_id: str,
    folder_in: schemas.FolderUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    folder = await crud.folder.get(db=db, entity_id=entity_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder doesn't exists")
    obj_in = {}
    if hasattr(folder_in, "folder_id") and folder_in.folder_id != 0:
        obj_in.setdefault("folder_id", folder_in.folder_id)

    if hasattr(folder_in, "name") and folder_in.name != "":
        obj_in.setdefault("name", folder_in.name)

    folder = await crud.folder.update(db, db_obj=folder, obj_in=obj_in)  # type: ignore

    return folder


@router.get("/{entity_id}", response_model=schemas.Folder)
async def read_folder_by_id(
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    folder = await crud.folder.get(db=db, entity_id=entity_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder doesn't exists")
    folder = await crud.folder.get(db, entity_id=entity_id)  # type: ignore

    return folder


@router.get("/", response_model=List[schemas.Folder])
async def read_folders(
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    _search = _get_search(q)
    if current_user["is_superuser"]:
        folders = await crud.folder.get_multi(db=db, skip=skip, limit=limit, search=_search)  # type: ignore
    else:
        folders = await crud.folder.get_multi_by_owner(db=db, owner_id=current_user["id"], skip=skip, limit=limit, search=_search)  # type: ignore

    return folders


@router.delete("/{entity_id}", response_model=schemas.Folder)
async def delete_folder(
    entity_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    folder = await crud.folder.get(db=db, entity_id=entity_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder doesn't exists")

    return await crud.folder.remove(db=db, entity_id=entity_id)


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"name": {"$regex": str(q)}},
            ]
        }
    return search
