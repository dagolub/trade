import asyncio
from time import sleep
import requests  # type: ignore
from app import crud
from app.api.api_v1.endpoints.deposits import _deposit
from app.db.session import database as db
from app.services.exchanger import Exchanger
from datetime import datetime
from app.crud.crud_deposit import (
    generate_random_string_passphrase,
    generate_random_small,
)


async def create_transaction(
    from_wallet, to_wallet, tx, amount, currency, type, owner_id, deposit_id
):
    await crud.transaction.create(
        db=db,
        obj_in={
            "owner_id": owner_id,
            "from_wallet": from_wallet,
            "to_wallet": to_wallet,
            "tx": tx,
            "amount": amount,
            "currency": currency,
            "type": type,
            "deposit_id": deposit_id,
            "created": datetime.utcnow(),
        },
    )


async def incoming_transaction():
    global status
    to_wallet = "TGuMUQ6y3Zc1kxdjE2A87zYYm94X8qmiJM"  # noqa
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    wallets = await crud.deposit.get_by_status(db=db, status="created")
    for wallet in wallets:
        deposit = await crud.deposit.get_by_wallet(db=db, wallet=wallet["wallet"])

        sub_account = deposit["sub_account"]
        passphrase = generate_random_string_passphrase(12)
        sub_account_api_keys = okx.create_sub_account_api_key(
            sub_account,
            sub_account + "L" + generate_random_small(5),
            passphrase=passphrase,
        )

        api_key = sub_account_api_keys["data"][0]["apiKey"]
        secret_key = sub_account_api_keys["data"][0]["secretKey"]

        deposit_history = okx.get_deposit_history(
            ccy="", api_key=api_key, secret=secret_key, passphrase=passphrase
        )

        for dh in deposit_history["data"]:
            if dh["to"] == wallet["wallet"]:
                amount = dh["amt"]
                currency = dh["ccy"]
                txId = dh["txId"]

                deposit_amount = okx.int_to_frac(wallet["sum"], wallet["currency"])
                if float(amount) < float(deposit_amount):
                    status = "partially"
                elif float(amount) > float(deposit_amount):
                    status = "overpayment"
                elif float(amount) == float(deposit_amount):
                    status = "paid"

                if currency == wallet["currency"]:
                    pass
                    await crud.deposit.update(
                        db=db, db_obj={"id": deposit["id"]}, obj_in={"status": status}
                    )
                    okx.transfer_money_to_main_account(
                        ccy=currency,
                        amt=amount,
                        sub_account=sub_account,
                    )
                    sleep(2)
                    await create_transaction(
                        from_wallet="<external>",
                        to_wallet=wallet["wallet"],
                        tx=txId,
                        amount=amount,
                        currency=currency,
                        type="OKX",
                        owner_id=deposit["owner_id"],
                        deposit_id=deposit["id"],
                    )
                    main_account = okx.transfer_money_to_main_account(
                        ccy=currency,
                        amt=amount,
                        from_account=18,  # trading account
                        sub_account=sub_account,
                        to_account=6,  # funding account
                        type_transfer=0,
                    )
                    sleep(2)

                    await create_transaction(
                        from_wallet=wallet["wallet"],
                        to_wallet="<internal>",
                        tx=main_account["data"][0]["transId"],
                        amount=amount,
                        currency=currency,
                        type="OKX",
                        owner_id=deposit["owner_id"],
                        deposit_id=deposit["id"],
                    )
                    user = await crud.user.get(db=db, entity_id=deposit["owner_id"])
                    if "bal" in user:
                        bal = user["bal"]
                    else:
                        bal = {}
                    if "bal" not in user:
                        bal = {
                            "btc": 0,
                            "ltc": 0,
                            "bch": 0,
                            "usdt": 0,
                            "etc": 0,
                            "eth": 0,
                        }

                    bal[currency.lower()] += float(amount)
                    await crud.user.update(db=db, db_obj=user, obj_in={"bal": bal})
                    #  auto exchange
        # if float(sub_account_balance["data"][0]["bal"]) > 0:
        #     main_account_balance = okx.get_account_balance(  # noqa
        #         ccy=sub_account_balance["data"][0]["ccy"]
        #     )
        #     sleep(2)
        # WHAT ?
        # transaction = okx.make_withdrawal(
        #     sub_account_balance["data"][0]["ccy"],
        #     main_account_balance["data"][0]["bal"],
        #     to_wallet,
        # )

        # await create_transaction(from_wallet="<internal>",
        #                          to_wallet=to_wallet,
        #                          tx=transaction['wdId'],
        #                          amount=sub_account_balance["data"][0]["bal"],
        #                          currency=sub_account_balance["data"][0]["ccy"],
        #                          type="OKX",
        #                          owner_id=deposit["owner_id"])


async def send_callback():
    wallets = await crud.deposit.get_by_status(db=db, status="paid")

    for wallet in wallets:
        if "callback" not in wallet:
            continue
        callback = wallet["callback"]

        if wallet["status"] == "paid":
            response = requests.post(callback, json=_deposit(wallet))
            callback_response = response.text

            _status = "in process"
            if response.status_code == 200:
                _status = "completed"
            await crud.callback.create(
                db=db,
                obj_in={
                    "owner_id": wallet["owner_id"],
                    "callback": callback,
                    "callback_response": callback_response,
                    "created": datetime.now(),
                },
            )
            await crud.deposit.update(
                db=db,
                db_obj={"id": wallet["id"]},
                obj_in={"callback_response": callback_response, "status": _status},
            )


async def fill_transaction():
    exchanger = Exchanger()
    okx = exchanger.get("OKX")

    transactions = await crud.transaction.get_not_filled(mongo_db=db)
    for trans in transactions:
        currency = trans["currency"]
        txid = trans["tx"]

        history = okx.get_withdrawal_history(currency, txid)
        if len(history["data"]) > 0:
            await crud.transaction.update(
                db=db, obj_in={"tx": history["data"][0]["txId"]}, db_obj=trans
            )


if __name__ == "__main__":
    asyncio.run(incoming_transaction())
    asyncio.run(send_callback())
    asyncio.run(fill_transaction())
