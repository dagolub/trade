import asyncio

import motor.motor_asyncio  # type: ignore

from trade.core.config import settings

MONGO_URL = f"{settings.MONGO_USER}:{settings.MONGO_PASS}@{settings.MONGO_HOST}"
if settings.MONGO_HOST == "localhost":
    MONGO_HOST = f"mongodb://{MONGO_URL}:27017/{settings.MONGO_DB}"
else:
    MONGO_HOST = f"mongodb+srv://{MONGO_URL}/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_HOST
)
client.get_io_loop = asyncio.get_event_loop
database = client[settings.MONGO_DB]
