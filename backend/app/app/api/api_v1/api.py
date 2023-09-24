from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    deposits,
    login,
    settings,
    transactions,
    users,
    wallets,
    withdraws,
    callbacks,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(deposits.router, prefix="/deposits", tags=["deposits"])
api_router.include_router(withdraws.router, prefix="/withdraws", tags=["withdraws"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)
api_router.include_router(wallets.router, prefix="/wallets", tags=["wallets"])
api_router.include_router(callbacks.router, prefix="/callbacks", tags=["callbacks"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
