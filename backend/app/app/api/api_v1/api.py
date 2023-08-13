from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login,
    users,
    deposits,
    transactions,
    wallets,
    settings,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(deposits.router, prefix="/deposits", tags=["deposits"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)
api_router.include_router(wallets.router, prefix="/wallets", tags=["wallets"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
