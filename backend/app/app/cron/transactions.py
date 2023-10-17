import asyncio
from time import sleep
import requests  # type: ignore
from app import crud
from app.api.api_v1.endpoints.deposits import _deposit as deposit
from app.db.session import database as db
from app.services.client import OKX
from datetime import datetime


async def create_transaction(
    from_wallet, to_wallet, tx, amount, currency, _type, owner_id, deposit_id, fee=0
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
            "type": _type,
            "fee": fee,
            "deposit_id": deposit_id,
            "created": datetime.utcnow(),
        },
    )


def delete_old_sub_account_api_keys(sub_account):
    print("Start delete")
    okx = OKX()
    sleep(2)
    api_keys = okx.get_sub_account_api_keys(sub_account)
    print("Delete api keys", api_keys)
    sleep(2)
    for i in api_keys["data"]:
        okx.delete_api_key(sub_account=sub_account, api_key=i["apiKey"])
        sleep(2)
    print("End delete")


async def incoming_transaction():  # noqa: 901
    okx = OKX()
    wallets = await crud.deposit.get_by_status(db=db, status=["created", "partially"])
    for wallet in wallets:
        sleep(2)
        print("")
        print("Wallet", wallet)
        _deposit = await crud.deposit.get_by_wallet(db=db, wallet=wallet["wallet"])

        sub_account = _deposit["sub_account"]
        delete_old_sub_account_api_keys(sub_account=sub_account)

        print("Before get key")
        try:
            sleep(1)
            sub_account_api_key = okx.create_sub_account_api_key(
                sub_account=sub_account
            )
            sleep(1)
            print("Sub account api key", sub_account_api_key)
            api_key = sub_account_api_key["data"][0]["apiKey"]
            secret = sub_account_api_key["data"][0]["secretKey"]
            passphrase = sub_account_api_key["data"][0]["passphrase"]
            deposit_history = okx.get_deposit_history(
                ccy="", api_key=api_key, secret=secret, passphrase=passphrase
            )
            sleep(1)
            for dh in deposit_history["data"]:
                print("DH", dh)
                if dh["to"] == wallet["wallet"]:
                    transaction = await crud.transaction.get_by_tx(db=db, tx=dh["txId"])

                    print("Transaction", transaction)
                    if transaction:
                        continue

                    amount = dh["amt"]
                    currency = dh["ccy"]
                    tx_id = dh["txId"]
                    obj_in = {
                        "status": wallet["status"] if "status" in wallet else "",
                        "paid": wallet["paid"] if "pre paid" in wallet else 0,
                    }

                    to_deposit = okx.fractional_to_integer(amount, wallet["currency"])

                    if "status" not in obj_in:
                        obj_in.setdefault("status", "partially")
                    if "paid" not in obj_in:
                        obj_in.setdefault("paid", to_deposit)
                    if "paid" in obj_in:
                        obj_in["paid"] = int(obj_in["paid"]) + int(to_deposit)

                    if int(obj_in["paid"]) < int(wallet["sum"]):
                        if "status" in obj_in:
                            obj_in["status"] = "partially"
                        else:
                            obj_in.setdefault("status", "partially")

                    if int(obj_in["paid"]) > int(wallet["sum"]):
                        if "status" in obj_in:
                            obj_in["status"] = "overpayment"
                        else:
                            obj_in.setdefault("status", "pre overpayment")

                    if int(obj_in["paid"]) == int(wallet["sum"]):
                        if "status" in obj_in:
                            obj_in["status"] = "pre paid"
                        else:
                            obj_in.setdefault("status", "pre paid")

                    if currency == wallet["currency"]:
                        print("Amount", amount)
                        print("Currency", currency)
                        print("tx_id", tx_id)
                        print("obj_in", obj_in)
                        await crud.deposit.update(
                            db=db,
                            db_obj={"id": _deposit["id"]},
                            obj_in=obj_in,
                        )
                        await create_corresponded_transactions(
                            okx=okx,
                            currency=currency,
                            amount=amount,
                            sub_account=sub_account,
                            wallet=wallet,
                            tx_id=tx_id,
                            _deposit=_deposit,
                        )
                        user = await crud.user.get(
                            db=db, entity_id=_deposit["owner_id"]
                        )
                        if "bal" in user:
                            bal = user["bal"]
                        else:
                            bal = {}
                        if "bal" not in user or not bal:
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
                else:
                    print("No wallets to update")
        except Exception as e:
            print("Exception in get sub account")
            print(e.args[0])
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


async def create_corresponded_transactions(
    okx, currency, amount, sub_account, wallet, tx_id, _deposit
):
    balance = okx.get_sub_account_balance(sub_account, currency)

    if len(balance["data"]) > 0 and int(balance["data"][0]["availBal"]) > 0:
        print("Balance", balance)
        okx.transfer_money_to_main_account(
            ccy=currency,
            amt=amount,
            sub_account=sub_account,
        )
        sleep(2)
        await create_transaction(
            from_wallet="<external>",
            to_wallet=wallet["wallet"],
            tx=tx_id,
            amount=amount,
            currency=currency,
            _type="OKX",
            owner_id=_deposit["owner_id"],
            deposit_id=_deposit["id"],
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
        print("Main account", main_account)
        await create_transaction(
            from_wallet=wallet["wallet"],
            to_wallet="<internal>",
            tx=main_account["data"][0]["transId"],
            amount=amount,
            currency=currency,
            _type="OKX",
            owner_id=_deposit["owner_id"],
            deposit_id=_deposit["id"],
        )


async def send_callback():  # noqa: 901
    wallets = await crud.deposit.get_by_status(
        db=db, status=["pre paid", "pre overpayment"]
    )

    for wallet in wallets:
        if "callback" not in wallet:
            continue
        callback = wallet["callback"]

        if wallet["status"] == "pre paid" or wallet["status"] == "pre overpayment":
            try:
                wallet["status"] = "paid"
                response = requests.post(callback, json=deposit(wallet))
                callback_response = response.text

                _status = "in process"
                if response.status_code == 200:
                    if wallet["status"] == "paid":
                        _status = "completed"
                    else:
                        _status = "completed-overpayment"
                await crud.callback.create(
                    db=db,
                    obj_in={
                        "owner_id": wallet["owner_id"],
                        "callback": callback,
                        "callback_response": callback_response,
                        "created": datetime.now(),
                        "deposit_id": wallet["id"],
                    },
                )
                await crud.deposit.update(
                    db=db,
                    db_obj={"id": wallet["id"]},
                    obj_in={"callback_response": callback_response, "status": _status},
                )
            except Exception as e:
                await crud.deposit.update(
                    db=db,
                    db_obj={"id": wallet["id"]},
                    obj_in={
                        "callback_response": str(e.args[0]),
                        "status": "complete no callback",
                    },
                )

    withdraws = await crud.withdraw.get_by_status(db=db, status="paid")

    for withdraw in withdraws:
        if "callback" not in withdraw:
            continue
        callback = withdraw["callback"]
        del withdraw["_id"]
        del withdraw["created"]
        if withdraw["status"] == "paid":
            response = requests.post(callback, json=withdraw)
            callback_response = response.text

            _status = "in process"
            if response.status_code == 200:
                _status = "completed"
            await crud.callback.create(
                db=db,
                obj_in={
                    "owner_id": withdraw["owner_id"],
                    "callback": callback,
                    "callback_response": callback_response,
                    "created": datetime.now(),
                },
            )
            await crud.withdraw.update(
                db=db,
                db_obj={"id": withdraw["id"]},
                obj_in={"callback_response": callback_response, "status": _status},
            )


async def fill_transaction():
    okx = OKX()
    transactions = await crud.transaction.get_not_filled(mongo_db=db)
    for trans in transactions:
        currency = trans["currency"]
        txid = trans["tx"]

        history = okx.get_withdrawal_history(currency, txid)
        if len(history["data"]) > 0:
            await crud.transaction.update(
                db=db, obj_in={"tx": history["data"][0]["txId"]}, db_obj=trans
            )


async def outgoing_transaction():
    okx = OKX()

    withdraws = await crud.withdraw.get_by_status(db=db, status="created")
    for withdraw in withdraws:
        currency = withdraw["currency"]
        chain = withdraw["chain"]
        amount = withdraw["sum"]
        to_wallet = withdraw["to"]
        owner_id = withdraw["owner_id"]
        fee = okx.get_currency_fee(_currency=currency, chain=chain)
        chain = okx.get_currency_chain(currency=currency, chain=chain)

        try:
            transaction = okx.make_withdrawal(
                amount=amount,
                address=to_wallet,
                currency=currency,
                chain=chain,
                fee=fee,
            )
            print("Withdraw", currency, chain, amount, to_wallet, fee, chain)
            await create_transaction(
                from_wallet="<internal>",
                to_wallet=to_wallet,
                tx=transaction["wdId"],
                amount=amount,
                currency=currency,
                _type="OKX",
                owner_id=owner_id,
                deposit_id="",
                fee=fee,
            )
            await crud.withdraw.update(
                db=db, db_obj={"id": withdraw["id"]}, obj_in={"status": "paid"}
            )

        except ValueError as e:
            print("Exception in outgoing transaction", e.args[0])
    return


if __name__ == "__main__":
    asyncio.run(incoming_transaction())
    asyncio.run(outgoing_transaction())
    asyncio.run(send_callback())
    asyncio.run(fill_transaction())
