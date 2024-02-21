import anyio
from trade.db.session import database as db
from datetime import datetime, timezone
from trade.schemas.volatility_mecx import VolatilityMECXCreate, VolatilityMECXUpdate
from trade.crud import volatility_mexc as crud


async def main():
    aggregation = [
        {"$match": {"to_coin": {"$eq": "USDT"}}},
        {
            "$match": {
                "$expr": {
                    "$gte": [
                        "$added",
                        {
                            "$dateSubtract": {
                                "startDate": "$$NOW",
                                "unit": "hour",
                                "amount": 24,
                            }
                        },
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": {"from_coin": "$from_coin", "to_coin": "$to_coin"},
                "avg": {"$avg": "$price"},
                "min": {"$min": "$price"},
            }
        },
        {"$match": {"min": {"$gt": 0}}},
        {"$project": {"diff": {"$divide": ["$avg", "$min"]}}},
    ]
    created = 0
    updated = 0
    async for pair in db.exchange_mecx.aggregate(aggregation):
        from_coin = pair.get("_id").get("from_coin")
        to_coin = pair.get("_id").get("to_coin")
        diff = pair.get("diff")

        if diff > 1.5:
            data = {
                "customer_id": 1,
                "to_coin": to_coin,
                "from_coin": from_coin,
                "price": round(float(diff), 5),
                "added": str(datetime.now(timezone.utc)),
            }
            pass
            db_obj = await crud.get_by_from_to(db, from_coin, to_coin)

            if db_obj:
                await crud.update(
                    db, db_obj=db_obj, obj_in=VolatilityMECXUpdate(**data)
                )
                updated += 1
            else:
                await crud.create(db, obj_in=[VolatilityMECXCreate(**data)])
                created += 1

    print("Updated: ", updated)
    print("Created: ", created)


if __name__ == "__main__":
    anyio.run(main)
