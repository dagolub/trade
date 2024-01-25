from typing import Any, List
import traceback
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from datetime import datetime
from app.services.client import OKX
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/estimate")
async def estimate(
    _from: str = Body(""),
    _to: str = Body(""),
    amount: float = Body(0),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> dict:
    okx = OKX()
    quota = okx.estimate_quota(
        from_ccy=_from,
        to_ccy=_to,
        side="sell",
        amount=amount,
    )
    obj_in = {
        "owmer_id": current_user["id"],
        "_from": _from,
        "_to": _to,
        "amount": amount,
        "quoteId": quota["quoteId"],
    }
    quota["_from"] = _from
    quota["_to"] = _to
    await crud.quota.create(
        db=db, obj_in={"id": quota["quoteId"], "data": quota, "ttl": datetime.now()}
    )
    await crud.exchange.create(db=db, obj_in=obj_in)
    return {"id": quota["quoteId"], "sec": float(quota["ttlMs"]) / 1000}


@router.post("/exchange", response_model=[])
async def exchange(
    _id: str = Body(""),
    _s: str = Body(""),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> dict:
    okx = OKX()
    quota = await crud.quota.get_by_id(db=db, id=_id)
    data = quota["data"]
    try:
        exchange = okx.convert_trade(
            from_ccy=data["baseCcy"],
            to_ccy=data["quoteCcy"],
            amount=data["rfqSz"],
            quota_id=data["quoteId"],
            side=data["side"],
        )
        user = await crud.user.get(db=db, entity_id=current_user["id"])
        user["bal"][data["baseCcy"]] = user["bal"][data["baseCcy"]] - data["_from"]
        user["bal"][data["quoteCcy"]] = user["bal"][data["baseCcy"]] + data["_to"]
        await crud.user.update(db=db, obj_in=user)
    except Exception:
        return "Can't create exchange"
    return exchange
