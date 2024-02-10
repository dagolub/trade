from typing import Any, List
import qrcode  # type: ignore
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.orm import Session  # type: ignore
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
import os
import shutil

router = APIRouter()
import re


@router.get("/count")
async def count(
    db: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.page.count(db=db, owner_id=owner_id, search=_search)


@router.post("/", response_model=schemas.Page)
async def create_page(
    title: str = Form(...),
    description: str = Form(...),
    document: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    page_in = {
        "owner_id": current_user["id"],
        "title": title,
        "description": description if description else "",
    }
    data = await document.read()
    match = re.search(r"\.([a-zA-Z0-9]+)$", document.filename)
    ext = match.group(1)
    page = await crud.page.create(db=db, obj_in=page_in)
    file = save_page(page["id"], data, ext)
    page = await crud.page.update(db=db, db_obj=page, obj_in={"file": file})
    return page


def save_page(id, data, ext):
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("files/tmp"):
        os.makedirs("files/tmp")
    if not os.path.exists("files/pages"):
        os.makedirs("files/pages")
    i = list(id)
    path = i[0] + i[1] + "/" + i[2] + i[3] + "/" + i[4] + i[5] + "/"
    path = (
        path
        + i[6]
        + i[7]
        + i[8]
        + i[9]
        + i[10]
        + i[11]
        + i[12]
        + i[13]
        + i[14]
        + i[15]
        + i[16]
        + i[17]
        + i[18]
        + i[19]
        + i[20]
        + i[21]
        + i[22]
        + i[23]
        + "/"
    )
    destination = f"files/pages/{path}"
    if not os.path.exists(destination):
        os.makedirs(destination)
    original = f"files/tmp/original.{ext}"
    with open(original, "wb") as file:
        file.write(data)

    result = destination + "document." + ext
    shutil.copy2(original, result)
    return "pages/" + path + "document." + ext


@router.put("/{entity_id}", response_model=schemas.Page)
async def update_page(
    entity_id: str,
    page_in: schemas.PageUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    page = await crud.page.get(db=db, entity_id=entity_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page doesn't exists")
    obj_in = {}

    if hasattr(page_in, "title") and page_in.title != "":
        obj_in.setdefault("title", page_in.title)
    if hasattr(page_in, "description") and page_in.description != "":
        obj_in.setdefault("description", page_in.description)

    page = await crud.page.update(db, db_obj=page, obj_in=obj_in)  # type: ignore

    return page


@router.get("/{entity_id}", response_model=schemas.Page)
async def read_page_by_id(
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    page = await crud.page.get(db=db, entity_id=entity_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page doesn't exists")
    page = await crud.page.get(db, entity_id=entity_id)  # type: ignore

    return page


@router.get("/", response_model=List[schemas.Page])
async def read_pages(
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    _search = _get_search(q)
    if current_user["is_superuser"]:
        pages = await crud.page.get_multi(db=db, skip=skip, limit=limit, search=_search)  # type: ignore
    else:
        pages = await crud.page.get_multi_by_owner(db=db, owner_id=current_user["id"], skip=skip, limit=limit, search=_search)  # type: ignore

    return pages


@router.delete("/{entity_id}", response_model=schemas.Page)
async def delete_page(
    entity_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    page = await crud.page.get(db=db, entity_id=entity_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page doesn't exists")

    return await crud.page.remove(db=db, entity_id=entity_id)


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"title": {"$regex": str(q)}},
                {"description": {"$regex": str(q)}},
            ]
        }
    return search
