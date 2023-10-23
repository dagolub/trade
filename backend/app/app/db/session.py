import asyncio

import motor.motor_asyncio  # type: ignore

from app.core.config import settings

if settings.MONGO_USER:
    MONGO_USERNAME = f"{settings.MONGO_USER}:{settings.MONGO_PASS}@"
else:
    MONGO_USERNAME = ""

MONGO_URL = f"{MONGO_USERNAME}{settings.MONGO_HOST}"
if settings.MONGO_HOST == "localhost" or settings.MONGO_HOST == "rpay-io-mongo1":
    MONGO_HOST = f"mongodb://{MONGO_URL}:27017/cryptopayments"
else:
    MONGO_HOST = f"mongodb+srv://{MONGO_URL}/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_HOST)
client.get_io_loop = asyncio.get_event_loop
database = client.cryptopayments
