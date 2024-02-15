from typing import Any, List, Optional
import os
import qrcode  # type: ignore
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session  # type: ignore
from datetime import datetime
from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
import shutil
import re
from app import crud
from boto3 import session
from boto3.s3.transfer import S3Transfer

router = APIRouter()


@router.get("/count")
async def count(
    db: Session = Depends(deps.get_db),
    q: str = "",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> int:
    _search = _get_search(q)
    owner_id = False if current_user["is_superuser"] else current_user["id"]
    return await crud.document.count(db=db, owner_id=owner_id, search=_search)


@router.get("/fill/{form_id}")
async def fill(
    form_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    page = await crud.page.get(db=db, entity_id=form_id)
    file = await crud.document.create(
        db=db,
        obj_in={"owner_id": current_user["id"], "name": page["title"], "folder_id": 0},
    )
    destination = create_dir(file["id"])
    _from = "files/" + page["file"]
    _to = destination + "document.pdf"
    shutil.copy2(_from, _to)
    await crud.document.update(
        db=db,
        db_obj=file,
        obj_in={"file": _to.replace("files/files/", "files/"), "ext": "pdf"},
    )
    return {"id": file["id"]}


def create_dir(id):
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
    destination = f"files/files/{path}"
    if not os.path.exists(destination):
        os.makedirs(destination)
    return destination


@router.post("/", response_model=schemas.Document)
async def create_document(
    document: UploadFile,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    data = await document.read()
    match = re.search(r"\.([a-zA-Z0-9]+)$", document.filename)
    ext = match.group(1)
    name = document.filename.replace(match.group(), "")
    obj_in = {
        "owner_id": current_user["id"],
        "name": name,
        "ext": ext,
        "created": datetime.utcnow(),
    }
    document = await crud.document.create(db=db, obj_in=obj_in)
    file = save_document(document["id"], data, ext)
    document = await crud.document.update(db=db, db_obj=document, obj_in={"file": file})
    return document


@router.put("/{entity_id}", response_model=schemas.Document)
async def update_document(
    entity_id: str,
    document: UploadFile,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    doc = await crud.document.get(db=db, entity_id=entity_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document doesn't exists")

    match = re.search(r"\.([a-zA-Z0-9]+)$", document.filename)
    data = await document.read()
    ext = match.group(1)
    file = save_document(doc["id"], data, ext)
    name = document.filename.replace(match.group(), "")
    obj_in = {"name": name, "ext": ext, "file": file}

    doc = await crud.document.update(db, db_obj=doc, obj_in=obj_in)  # type: ignore

    return doc


@router.get("/{entity_id}", response_model=schemas.Document)
async def read_document_by_id(
    entity_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    document = await crud.document.get(db=db, entity_id=entity_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document doesn't exists")
    document = await crud.document.get(db, entity_id=entity_id)  # type: ignore
    document["file"] = settings.FILES_HOST + document["file"]
    return document


@router.get("/", response_model=List[schemas.Document])
async def read_documents(
    skip: int = 0,
    limit: int = 100,
    q: str = "",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),  # noqa
) -> Any:
    _search = _get_search(q)
    if current_user["is_superuser"]:
        documents = await crud.document.get_multi(db=db, skip=skip, limit=limit, search=_search)  # type: ignore
    else:
        documents = await crud.document.get_multi_by_owner(db=db, owner_id=current_user["id"], skip=skip, limit=limit, search=_search)  # type: ignore
    result = []
    for document in documents:
        document["file"] = (
            settings.FILES_HOST + document["file"] if "file" in document else ""
        )
        result.append(document)
    return result


@router.delete("/{entity_id}", response_model=schemas.Document)
async def delete_document(
    entity_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    document = await crud.document.get(db=db, entity_id=entity_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document doesn't exists")

    return await crud.document.remove(db=db, entity_id=entity_id)


def _get_search(q: str = ""):
    search = {}
    if q != "":
        search = {
            "$or": [
                {"name": {"$regex": str(q)}},
            ]
        }
    return search


def save_document(id, data, ext):
    if not os.path.exists("files"):
        os.makedirs("files")
    if not os.path.exists("files/tmp"):
        os.makedirs("files/tmp")

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
    destination = f"files/{path}"
    if not os.path.exists(destination):
        os.makedirs(destination)
    original = f"files/tmp/original.{ext}"
    with open(original, "wb") as file:
        file.write(data)

    result = destination + "document." + ext
    if settings.FILES_KEY and settings.FILES_SECRET:
        s = session.Session()
        client = s.client(
            "s3",
            region_name="fra1",  # enter your own region_name
            endpoint_url="https://pdfmax.fra1.digitaloceanspaces.com",  # enter your own endpoint url
            aws_access_key_id=settings.FILES_KEY,
            aws_secret_access_key=settings.FILES_SECRET,
        )

        transfer = S3Transfer(client)

        # Uploads a file called 'name-of-file' to your Space called 'name-of-space'
        # Creates a new-folder and the file's final name is defined as 'name-of-file'
        transfer.upload_file(original, "files", f"{path}document.{ext}")

        # This makes the file you are have specifically uploaded public by default.
        response = client.put_object_acl(
            ACL="public-read",
            Bucket="files",
            Key=f"{path}document.{ext}",
        )
        return "files/" + path + "document." + ext

    # delete tmp file

    shutil.copy2(original, result)
    return path + "document." + ext
