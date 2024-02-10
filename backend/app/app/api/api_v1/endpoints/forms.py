from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app import crud

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def forms(db: Session = Depends(deps.get_db)):
    pages = await crud.page.get_multi(db=db, skip=0, limit=1000)
    result = ""
    for page in pages:
        url = page["title"].lower().replace(" ", "_") + ".html"
        result += f'<a href="{url}">{page["title"]}</a><br />'

    return result


@router.get("/fill/online?id={id}")
async def fill(id: int, db: Session = Depends(deps.get_db)):
    id
    pass


@router.get("/{slug}", response_class=HTMLResponse)
async def forms(slug: str, db: Session = Depends(deps.get_db)):
    title = slug.replace(".html", "").title().replace("_", " ")
    page = await crud.page.get_by_title(db=db, title=title)
    url = "/forms/fill/online?id=" + page[0]["id"]
    return f'<a href="{url}">Fill online</a>'
