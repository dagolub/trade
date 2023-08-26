import asyncio
from time import sleep

from app import crud
from app.db.session import database as db
from app.services.exchanger import Exchanger


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
        },
    )


async def incoming_transaction():
    to_wallet = "TGuMUQ6y3Zc1kxdjE2A87zYYm94X8qmiJM"  # noqa
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    wallets = await crud.deposit.get_by_status(db=db, status="in progress")
    for wallet in wallets:
        deposit = await crud.deposit.get_by_wallet(
            db=db, wallet="TGqENrsSTFycMVYUKyueBwU1gjd4FKAaao"
        )
        await crud.deposit.update(
            db=db, db_obj={"id": deposit["id"]}, obj_in={"status": "paid"}
        )
        sub_account = deposit["sub_account"]
        api_key = deposit["sub_account_api_key"]
        secret_key = deposit["sub_account_secret_key"]
        passphrase = deposit["sub_account_passphrase"]
        sub_account = "OleskBackendwxrmg"
        api_key = "a6e41935-78bf-45c6-b133-5fe6c451d36f"
        secret_key = "BCFA403455231F0321D9607066806BDE"
        passphrase = "KY7nyl*4!tria8bD"

        sub_account_balance = okx.get_account_balance(
            deposit["currency"], api_key, secret_key, passphrase
        )
        if float(sub_account_balance["data"][0]["bal"]) > 0:
            balance = okx.transfer_money_to_main_account(
                ccy=sub_account_balance["data"][0]["ccy"],
                amt=sub_account_balance["data"][0]["bal"],
                sub_account=sub_account,
            )
            sleep(2)

            await create_transaction(
                from_wallet="<external>",
                to_wallet=wallet["wallet"],
                tx=balance["data"][0]["transId"],
                amount=sub_account_balance["data"][0]["bal"],
                currency=sub_account_balance["data"][0]["ccy"],
                type="OKX",
                owner_id=deposit["owner_id"],
                deposit_id=deposit["id"],
            )

            main_account = okx.transfer_money_to_main_account(
                ccy=sub_account_balance["data"][0]["ccy"],
                amt=sub_account_balance["data"][0]["bal"],
                from_account=18,
                sub_account=sub_account,
                to_account=6,
                type_transfer=0,
            )
            sleep(2)

            await create_transaction(
                from_wallet=wallet["wallet"],
                to_wallet="<internal>",
                tx=main_account["data"][0]["transId"],
                amount=sub_account_balance["data"][0]["bal"],
                currency=sub_account_balance["data"][0]["ccy"],
                type="OKX",
                owner_id=deposit["owner_id"],
                deposit_id=deposit["id"],
            )

            main_account_balance = okx.get_account_balance(  # noqa
                ccy=sub_account_balance["data"][0]["ccy"]
            )
            sleep(2)
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
    asyncio.run(fill_transaction())
