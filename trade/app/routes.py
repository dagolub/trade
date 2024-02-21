from fastapi import APIRouter, Body
from trade.core.deps import get_db
from sqlalchemy.orm import Session  # type: ignore
from fastapi import Depends

router = APIRouter()


@router.get("/operations")
async def operations():

    return {"success": "OK"}


@router.get("/start")
async def start(
    exchanger: str = Body(),
    start_coin: str = Body(),
    amount: float = Body(),
    db: Session = Depends(get_db),
):
    return {"success": "OK"}


@router.get("/callback")
async def callback():

    return {"success": "OK"}


@router.get("/exchangers")
async def exchangers():

    return ["Binance", "OKX"]
