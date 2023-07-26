from app.services.exchanger import Exchanger
import asyncio
import random
import string
from app.core.config import settings


def generate_random_string_passphrase(length):
    letters = "1234567890" + string.ascii_uppercase + string.ascii_lowercase + "!@#$%^&*()"
    return ''.join(random.choice(letters) for i in range(length))


async def incoming_transaction():
    to_wallet = 'TGuMUQ6y3Zc1kxdjE2A87zYYm94X8qmiJM'
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    sub_account = "posteruwjyq"
    sub_account_label = sub_account + "Label4"
    passphrase = '2wltCd$&S!'
    api_key = 'fe4c45c3-f21c-4748-a6a3-aef630c4f0bb'
    secret_key = '0C181CA10505E321BEF1B06849DEFCEA'
    # okx = okx.create_sub_account_api_key(sub_account, sub_account_label, passphrase)
    sub_account_balance = okx.get_account_balance(api_key, secret_key, passphrase, "USDT")
    if int(sub_account_balance["data"][0]["bal"]) > 0:
        balance = okx.transfer_money_to_main_account(ccy=sub_account_balance["data"][0]["ccy"],
                                                     amt=sub_account_balance["data"][0]["bal"],
                                                     sub_account=sub_account)
        txid = balance["data"][0]["transId"]
        pass
    main_account = okx.transfer_money_to_main_account(ccy="USDT",
                                                      amt=9.003,
                                                      from_account=18,
                                                      sub_account=sub_account,
                                                      to_account=6,
                                                      type_transfer=0)
    transaction = okx.make_withdrawal("USDT", 9.003, to_wallet)
    pass


if __name__ == "__main__":
    asyncio.run(incoming_transaction())
