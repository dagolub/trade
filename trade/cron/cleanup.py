import anyio
from trade.db.session import database as db
from datetime import datetime
from trade import crud


async def main():
    aggregation = [
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d-%H", "date": "$added"}},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": -1}},
    ]
    deleted = 0

    total = 0
    delete_from_date = None
    async for pair in db.exchange_mecx.aggregate(aggregation):
        total += pair.get("count")
        if total > 500000:
            delete_from_date = pair.get("_id")
            break

    if delete_from_date:
        date = datetime.strptime(delete_from_date, "%Y-%m-%d-%H")

        result = await crud.exchange_mecx.remove(db, {"added": {"$lt": date}})
        deleted += result.deleted_count

    result_usdt = await crud.exchange_mecx.remove(db, {"to_coin": {"$ne": "USDT"}})
    deleted += result_usdt.deleted_count

    total = 0
    delete_from_date = None
    async for pair in db.exchange_okx.aggregate(aggregation):
        total += pair.get("count")
        if total > 500000:
            delete_from_date = pair.get("_id")
            break

    if delete_from_date:
        date = datetime.strptime(delete_from_date, "%Y-%m-%d-%H")

        result = await crud.exchange_okx.remove(db, {"added": {"$lt": date}})
        deleted += result.deleted_count

    result_usdt = await crud.exchange_okx.remove(db, {"to_coin": {"$ne": "USDT"}})
    deleted += result_usdt.deleted_count

    total = 0
    delete_from_date = None
    async for pair in db.exchange_binance.aggregate(aggregation):
        total += pair.get("count")
        if total > 500000:
            delete_from_date = pair.get("_id")
            break

    if delete_from_date:
        date = datetime.strptime(delete_from_date, "%Y-%m-%d-%H")

        result = await crud.exchange_binance.remove(db, {"added": {"$lt": date}})
        deleted += result.deleted_count

    result_usdt = await crud.exchange_binance.remove(db, {"to_coin": {"$ne": "USDT"}})
    deleted += result_usdt.deleted_count

    print("Deleted: ", deleted)


if __name__ == "__main__":
    anyio.run(main)
