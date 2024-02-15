from fastapi import APIRouter, Depends
from app.api import deps
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from app import crud
from app.core.config import settings

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def forms(db: Session = Depends(deps.get_db)):
    pages = await crud.page.get_multi(db=db, skip=0, limit=1000)
    result = ""
    for page in pages:
        url = page["title"].lower().replace(" ", "_") + ".html"
        result += f'<a href="{url}">{page["title"]}</a><br />'

    return result


@router.get("/fill/online/{form_id}", response_class=HTMLResponse)
async def fill(form_id, db: Session = Depends(deps.get_db)):
    host = None

    if settings.ENVIRONMENT == "local":
        host = "http://pdfmax.localhost"
    if settings.ENVIRONMENT == "stage":
        host = "http://pdfmax.xyz"

    return RedirectResponse(f"{host}/fill?id=" + form_id)


@router.get("/{slug}", response_class=HTMLResponse)
async def forms(slug: str, db: Session = Depends(deps.get_db)):
    title = slug.replace(".html", "").title().replace("_", " ")
    page = await crud.page.get_by_title(db=db, title=title)
    url = "/forms/fill/online/" + page[0]["id"]
    return f'<a href="{url}">Fill online</a>'
