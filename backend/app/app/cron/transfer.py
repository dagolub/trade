import asyncio
import random
import string

from app.services.exchanger import Exchanger


def generate_random_string_passphrase(length):
    letters = (
        "1234567890" + string.ascii_uppercase + string.ascii_lowercase + "!@#$%^&*()"
    )
    return "".join(random.choice(letters) for i in range(length))


async def incoming_transaction():
    to_wallet = "TGuMUQ6y3Zc1kxdjE2A87zYYm94X8qmiJM"
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    tx = okx.get_withdrawal_history("USDT", 98842367)
    pass


if __name__ == "__main__":
    asyncio.run(incoming_transaction())
