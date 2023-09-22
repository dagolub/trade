from app.services.okx_client import OKX
import time
import string
import random


def generate_random_ints(length):
    letters = "01234567890"
    return "".join(random.choice(letters) for i in range(length))


def generate_random_small(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_big(length):
    letters = string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_string_passphrase(length):
    letters = "!@#$%^&*()[]/?;':.,<>|-_=+`~"
    random_int = generate_random_ints(4)
    random_string = generate_random_small(2) + generate_random_big(2) + random_int
    return random_string.join(random.choice(letters) for i in range(length - 8))


sub_accounts = [
    "OPrjdNGD",
    "OBrugHDJ",
    "OBnbdVSD",
    "OByyxDYQ",
    "OBdatSII",
    "OBagoPET",
    "OBxmrATA",
]

if __name__ == "__main__":
    for sub_account in sub_accounts:
        okx = OKX()
        passphrase = generate_random_string_passphrase(12)
        sub_account_api_keys = okx.create_sub_account_api_key(
            sub_account,
            sub_account + "L" + generate_random_small(6),
            passphrase=passphrase,
        )
        time.sleep(2)
        if len(sub_account_api_keys["data"]) == 0:
            print(sub_account)
            print(sub_account_api_keys)
        else:
            sub_account_balance = okx.get_account_balance(
                "USDT",
                sub_account_api_keys["data"][0]["apiKey"],
                sub_account_api_keys["data"][0]["secretKey"],
                sub_account_api_keys["data"][0]["passphrase"],
            )
            time.sleep(2)
            # print(sub_account_api_keys)
            # print(sub_account_balance)
            if float(sub_account_balance["data"][0]["bal"]) > 0:
                balance = okx.transfer_money_to_main_account(
                    ccy=sub_account_balance["data"][0]["ccy"],
                    amt=sub_account_balance["data"][0]["bal"],
                    sub_account=sub_account,
                )
