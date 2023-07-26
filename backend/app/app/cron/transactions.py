from time import sleep
from app.db.session import database as db
from app.services.exchanger import Exchanger
import asyncio
from app import crud

async def create_transaction(from_wallet, to_wallet, tx, amount, currency, type, owner_id):
    await crud.transaction.create(db=db, obj_in={
        "owner_id": owner_id,
        "from_wallet": from_wallet,
        "to_wallet": to_wallet,
        "tx": tx,
        "amount": amount,
        "currency": currency,
        "type": type
    })
async def incoming_transaction():
    to_wallet = 'TGuMUQ6y3Zc1kxdjE2A87zYYm94X8qmiJM'
    exchanger = Exchanger()
    okx = exchanger.get("OKX")
    wallets = await crud.deposit.get_by_status(db=db, status="waiting")
    for wallet in wallets:
        deposit = await crud.deposit.get_by_wallet(db=db, wallet=wallet["wallet"])
        await crud.deposit.update(db=db, db_obj={"id": deposit["id"]}, obj_in={"status": "paid"})
        sub_account = deposit["sub_account"]
        api_key = deposit["sub_account_api_key"]
        secret_key = deposit["sub_account_secret_key"]
        passphrase = deposit["sub_account_passphrase"]

        sub_account_balance = okx.get_account_balance("USDT", api_key, secret_key, passphrase)
        if float(sub_account_balance["data"][0]["bal"]) > 0:
            balance = okx.transfer_money_to_main_account(ccy=sub_account_balance["data"][0]["ccy"],
                                                         amt=sub_account_balance["data"][0]["bal"],
                                                         sub_account=sub_account)
            sleep(2)
            txid = balance["data"][0]["transId"]
            await create_transaction(from_wallet="<external>",
                                     to_wallet=wallet["wallet"],
                                     tx=txid,
                                     amount=sub_account_balance["data"][0]["bal"],
                                     currency=sub_account_balance["data"][0]["ccy"],
                                     type="OKX",
                                     owner_id=deposit["owner_id"])
            main_account = okx.transfer_money_to_main_account(ccy="USDT",
                                                              amt=sub_account_balance["data"][0]["bal"],
                                                              from_account=18,
                                                              sub_account=sub_account,
                                                              to_account=6,
                                                              type_transfer=0)
            sleep(2)
            await create_transaction(from_wallet=wallet["wallet"],
                                     to_wallet="<internal>",
                                     tx=main_account["data"][0]["transId"],
                                     amount=sub_account_balance["data"][0]["bal"],
                                     currency=sub_account_balance["data"][0]["ccy"],
                                     type="OKX",
                                     owner_id=deposit["owner_id"])
            main_account_balance = okx.get_account_balance(ccy="USDT")
            sleep(2)
            transaction = okx.make_withdrawal("USDT", main_account_balance["data"][0]["bal"], to_wallet)
            await create_transaction(from_wallet="<internal>",
                                     to_wallet=to_wallet,
                                     tx=transaction['wdId'],
                                     amount=sub_account_balance["data"][0]["bal"],
                                     currency=sub_account_balance["data"][0]["ccy"],
                                     type="OKX",
                                     owner_id=deposit["owner_id"])

if __name__ == "__main__":
    asyncio.run(incoming_transaction())
