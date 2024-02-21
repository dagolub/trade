import anyio
from trade.db.session import database as db


async def main():
    aggregation = [{"$sort": {"price": -1}}, {"$limit": 10}]

    async for pair in db.volatility_mecx.aggregate(aggregation):
        print(pair.get("from_coin"), pair.get("to_coin"), pair.get("price"))


if __name__ == "__main__":
    anyio.run(main)
