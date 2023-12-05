import asyncio
from time import sleep
import requests  # type: ignore
from app import crud
from app.api.api_v1.endpoints.deposits import _deposit as deposit
from app.db.session import database as db
from app.services.client import OKX
from datetime import datetime
import traceback
from decimal import Decimal
from app import schemas


async def get_superuser() -> schemas.User:
    email = await crud.user.get_by_email(
        db=db, email="admin@cryptopayments.fastapi.xyz"
    )
    if not email:
        email = await crud.user.get_by_email(db=db, email="admin@rpay.io")
    if not email:
        return False
    return email


async def create_transaction(
    from_wallet,
    to_wallet,
    tx,
    amount,
    currency,
    _type,
    owner_id="",
    deposit_id="",
    withdraw_id="",
    fee=0.0,
):
    return await crud.transaction.create(
        db=db,
        obj_in={
            "from_wallet": from_wallet,
            "to_wallet": to_wallet,
            "tx": tx,
            "amount": amount,
            "currency": currency,
            "type": _type,
            "fee": fee,
            "owner_id": owner_id,
            "deposit_id": deposit_id,
            "withdraw_id": withdraw_id,
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
                        "paid": wallet["paid"] if "paid" in wallet else 0,
                    }

                    to_deposit = okx.fractional_to_integer(amount, wallet["currency"])
                    if int(wallet["sum"]) == 0:
                        wallet["sum"] = okx.fractional_to_integer(
                            dh["amt"], wallet["currency"]
                        )
                        obj_in["sum"] = okx.fractional_to_integer(
                            dh["amt"], wallet["currency"]
                        )
                        fee = 0
                        if dh["amt"]:
                            user = await crud.user.get(
                                db=db, entity_id=wallet["owner_id"]
                            )
                            if (
                                "commissions" in user
                                and wallet["currency"].lower()
                                in user["commissions"]  # noqa
                            ):
                                comm = user["commissions"][wallet["currency"].lower()][
                                    "in"
                                ]
                            else:
                                comm = {"percent": 0, "fixed": 0}
                            fee = okx.fractional_to_integer(
                                float(dh["amt"]) * 0.0100 * float(comm["percent"])
                                + float(comm["fixed"]),  # noqa
                                wallet["currency"].lower(),
                            )
                        obj_in["fee"] = fee
                    if "status" not in obj_in:
                        obj_in.setdefault("status", "partially")
                    if "paid" not in obj_in:
                        obj_in.setdefault("paid", to_deposit)
                    if "paid" in obj_in:
                        obj_in["paid"] = int(obj_in["paid"]) + int(to_deposit)

                    if float(obj_in["paid"]) < float(wallet["sum"]):
                        if "status" in obj_in:
                            obj_in["status"] = "partially"
                        else:
                            obj_in.setdefault("status", "partially")

                    if float(obj_in["paid"]) > float(wallet["sum"]):
                        if "status" in obj_in:
                            obj_in["status"] = "pre overpayment"
                        else:
                            obj_in.setdefault("status", "pre overpayment")

                    if float(obj_in["paid"]) == float(wallet["sum"]):
                        if "status" in obj_in:
                            obj_in["status"] = "pre paid"
                        else:
                            obj_in.setdefault("status", "pre paid")

                    if currency == wallet["currency"]:
                        print("Amount", amount)
                        print("Currency", currency)
                        print("tx_id", tx_id)
                        print("obj_in", obj_in)
                        transaction = await create_corresponded_transactions(
                            okx=okx,
                            currency=currency,
                            amount=amount,
                            sub_account=sub_account,
                            wallet=wallet,
                            tx_id=tx_id,
                            _deposit=_deposit,
                        )
                        if transaction:
                            await crud.deposit.update(
                                db=db,
                                db_obj={"id": _deposit["id"]},
                                obj_in=obj_in,
                            )

                            user = await crud.user.get(
                                db=db, entity_id=_deposit["owner_id"]
                            )

                            if (
                                "commissions"
                                and currency.lower() in user["commissions"]  # noqa
                            ):
                                comm = user["commissions"][currency.lower()]["in"]
                            else:
                                comm = {"fixed": 0, "percent": 0}
                            if comm:
                                admin_amount = okx.integer_to_fractional(
                                    _deposit["fee"], _deposit["currency"].lower()
                                )
                                amount = Decimal(str(amount)) - Decimal(
                                    str(admin_amount)
                                )

                                super_user = await get_superuser()
                                if super_user:
                                    #  update super user balance
                                    if "bal" not in super_user:
                                        super_user["bal"] = {
                                            "btc": 0,
                                            "ltc": 0,
                                            "usdt": 0,
                                            "eth": 0,
                                        }
                                    if (
                                        "bal" in super_user
                                        and currency.lower()  # noqa
                                        in super_user["bal"]  # noqa
                                    ):
                                        new_admin_balance = float(
                                            super_user["bal"][currency.lower()]
                                        ) + float(
                                            admin_amount
                                        )  # noqa
                                    else:
                                        new_admin_balance = admin_amount

                                    await crud.user.update(
                                        db=db,
                                        db_obj={"id": super_user["id"]},
                                        obj_in={
                                            "bal": {currency.lower(): new_admin_balance}
                                        },
                                    )
                            fee = _deposit["fee"]
                            if fee > 0:
                                await create_transaction(
                                    from_wallet="<internal>",
                                    to_wallet="<commission>",
                                    currency=_deposit["currency"],
                                    tx="",
                                    amount=0,
                                    _type="OKX",
                                    fee=fee,
                                    owner_id=_deposit["owner_id"],
                                    deposit_id=_deposit["id"],
                                )

                            if "bal" in user:
                                bal = user["bal"]
                            else:
                                bal = {}
                            if "bal" not in user or not bal:
                                bal = {
                                    "btc": 0.0,
                                    "ltc": 0.0,
                                    "usdt": 0.0,
                                    "eth": 0.0,
                                }

                            bal[currency.lower()] = float(
                                bal[currency.lower()]
                            ) + float(amount)

                            await crud.user.update(
                                db=db, db_obj=user, obj_in={"bal": bal}
                            )
                else:
                    print("No wallets to update")
        except Exception as e:
            print("Exception in get sub account")
            print(e)
            traceback.print_exc()


async def create_corresponded_transactions(
    okx, currency, amount, sub_account, wallet, tx_id, _deposit
):
    balance = okx.get_sub_account_balance(sub_account, currency)
    print("Balance", balance)
    transactions = 0
    if len(balance["data"]) > 0 and float(balance["data"][0]["availBal"]) > 0:
        print("Balance", balance, balance["data"][0])
        okx.transfer_money_to_main_account(
            ccy=currency,
            amt=amount,
            sub_account=sub_account,
        )
        sleep(2)
        transaction = await create_transaction(
            from_wallet="<external>",
            to_wallet=wallet["wallet"],
            tx=tx_id,
            amount=amount,
            currency=currency,
            _type="OKX",
            owner_id=_deposit["owner_id"],
            deposit_id=_deposit["id"],
        )
        if transaction:
            transactions = transactions + 1
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
        transaction = await create_transaction(
            from_wallet=wallet["wallet"],
            to_wallet="<internal>",
            tx=main_account["data"][0]["transId"],
            amount=amount,
            currency=currency,
            _type="OKX",
            owner_id=_deposit["owner_id"],
            deposit_id=_deposit["id"],
        )
        if transaction:
            transactions = transactions + 1

        if transactions == 2:
            return True
    return False


async def exchange():
    wallets = await crud.deposit.get_by_regex(
        db=db, search={"status": {"$regex": "(pre paid|pre overpayment)"}}
    )
    for wallet in wallets:
        await crud.deposit.update(
            db=db,
            db_obj={"id": wallet["id"]},
            obj_in={"status": wallet["status"].replace("pre", "aex")},
        )

        user = await crud.user.get(db=db, entity_id=wallet["owner_id"])
        if (
            wallet["currency"] != "USDT"  # noqa
            and "autotransfer" in user  # noqa
            and user["autotransfer"]  # noqa
        ):
            # get quota
            await exchange_usdt(wallet)


async def exchange_usdt(wallet):
    okx = OKX()
    amount = float(
        okx.integer_to_fractional(wallet["sum"], wallet["currency"])
    ) - float(okx.integer_to_fractional(wallet["fee"], wallet["currency"]))
    quota = okx.estimate_quota(
        from_ccy=wallet["currency"],
        to_ccy="USDT",
        side="sell",
        amount=amount,
    )
    if quota and "baseCcy" in quota:
        exchange = okx.convert_trade(
            from_ccy=quota["baseCcy"],
            to_ccy=quota["quoteCcy"],
            amount=quota["rfqSz"],
            quota_id=quota["quoteId"],
            side=quota["side"],
        )

        if len(exchange.get("data")) > 0:
            exchange_data = exchange.get("data")[0]
            usdt = str(
                Decimal(str(exchange_data["fillPx"]))  # noqa
                * Decimal(str(exchange_data["fillBaseSz"]))  # noqa
            )
            print("USDT: ", usdt)

            obj_in = {
                "deposit_id": wallet["id"],
                "currency": wallet["currency"],
                "rate": exchange_data["fillPx"],
                "usdt": usdt,
                "created": datetime.utcnow(),
            }
            await crud.exchange.create(db=db, obj_in=obj_in)

            # update balance
            u = await crud.user.get(db=db, entity_id=wallet["owner_id"])
            if "bal" in u:
                user = {"bal": u["bal"]}
            else:
                user = {"bal": {"btc": 0.0, "ltc": 0.0, "eth": 0.0, "usdt": 0.0}}
            user["bal"][quota["baseCcy"].lower()] = str(
                Decimal(str(user["bal"][quota["baseCcy"].lower()]))
                - Decimal(str(quota["rfqSz"]))  # noqa
            )
            user["bal"]["usdt"] = float(user["bal"]["usdt"]) + float(usdt)
            await crud.user.update(db=db, db_obj=u, obj_in=user)


async def send_callback():  # noqa: 901
    wallets = await crud.deposit.get_by_regex(
        db=db,
        search={"status": {"$regex": "(paid|overpayment)"}},
    )

    for wallet in wallets:
        if "callback" not in wallet:
            continue

        if wallet["status"].split(" ")[0] in ["pre", "aex"]:
            print("Wallet status", wallet["status"])
            if "pre" in wallet["status"]:
                print("Pre status", wallet["status"])
                continue

            if "aex" in wallet["status"]:
                try:
                    await send_callback_aex(wallet)
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
        try:
            await send_callback_withdraw(withdraw)
        except Exception as e:
            await crud.withdraw.update(
                db=db,
                db_obj={"id": withdraw["id"]},
                obj_in={
                    "callback_response": str(e.args[0]),
                    "status": "complete no callback",
                },
            )


async def send_callback_withdraw(withdraw):
    if "callback" not in withdraw:
        return False
    callback = withdraw["callback"]
    del withdraw["_id"]
    del withdraw["created"]
    if "paid" in withdraw["status"]:
        response = requests.post(callback, json=withdraw)
        callback_response = response.text

        _status = withdraw["status"]
        if response.status_code == 200 and withdraw["status"] == "paid":
            _status = "completed"
        await crud.callback.create(
            db=db,
            obj_in={
                "owner_id": withdraw["owner_id"],
                "callback": callback,
                "callback_response": callback_response,
                "withdraw_id": withdraw["id"],
                "created": datetime.now(),
            },
        )
        await crud.withdraw.update(
            db=db,
            db_obj={"id": withdraw["id"]},
            obj_in={"callback_response": callback_response, "status": _status},
        )
        return True


async def send_callback_aex(wallet):
    print("Aex status", wallet["status"])
    wallet["status"] = (
        "paid" if wallet["status"] == "aex paid" else "overpayment"  # noqa  # noqa
    )
    exchange = await crud.exchange.get_by_deposit(db=db, deposit_id=wallet["id"])
    if exchange:
        print("Exchange", exchange)
        del exchange["_id"]
        del exchange["created"]
        wallet["exchange"] = exchange
    else:
        print("Exchange", exchange)
    response = requests.post(wallet["callback"], json=deposit(wallet))
    callback_response = response.text

    _status = "in process"
    if response.status_code == 200:
        if wallet["status"] == "paid":
            _status = "completed"
        else:
            _status = "c-overpayment"
    else:
        pass
    await crud.callback.create(
        db=db,
        obj_in={
            "owner_id": wallet["owner_id"],
            "callback": wallet["callback"],
            "callback_response": callback_response,
            "created": datetime.now(),
            "deposit_id": wallet["id"],
        },
    )
    await crud.deposit.update(
        db=db,
        db_obj={"id": wallet["id"]},
        obj_in={
            "callback_response": callback_response,
            "status": _status,
        },
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
        network_fee = okx.get_currency_fee(_currency=currency, chain=chain)
        chain = okx.get_currency_chain(currency=currency, chain=chain)
        user = await crud.user.get(db=db, entity_id=withdraw["owner_id"])
        comm = {"percent": 0, "fixed": 0}
        if (
            "commissions" in user
            and currency.lower() in user["commissions"]  # noqa
            and "out" in user["commissions"][currency.lower()]  # noqa
        ):
            comm = user["commissions"][currency.lower()]["out"]
        fee = float(amount) * 0.0100 * float(comm["percent"]) + float(comm["fixed"])
        try:
            transaction = okx.make_withdrawal(
                amount=float(amount) + float(network_fee),
                address=to_wallet,
                currency=currency,
                chain=chain,
                fee=network_fee,
            )
            print(
                "Withdraw", currency, chain, amount, to_wallet, fee, network_fee, chain
            )
            await create_transaction(
                from_wallet="<internal>",
                to_wallet=to_wallet,
                tx=transaction["wdId"],
                amount=amount,
                currency=currency,
                _type="OKX",
                owner_id=owner_id,
                fee=0,
                withdraw_id=withdraw["id"],
            )
            await create_transaction(
                from_wallet="<internal>",
                to_wallet="<commission>",
                currency=currency,
                tx="",
                amount=0,
                _type="OKX",
                fee=fee,
                owner_id=owner_id,
                withdraw_id=withdraw["id"],
            )
            await crud.withdraw.update(
                db=db,
                db_obj={"id": withdraw["id"]},
                obj_in={
                    "status": "paid",
                    "network_fee": network_fee,
                },
            )
            super_user = await get_superuser()
            if "bal" in super_user:
                super_user_bal = super_user["bal"]
            else:
                super_user_bal = {"btc": 0, "eth": 0, "ltc": 0, "usdt": 0}
            if currency.lower() in super_user_bal:
                current_balance = super_user_bal[currency.lower()]
            else:
                current_balance = 0

            super_user_bal[currency.lower()] = (
                Decimal(str(current_balance))
                + Decimal(str(fee))  # noqa
                - Decimal(str(network_fee))  # noqa
            )

            await crud.user.update(
                db=db,
                db_obj={"id": super_user["id"]},
                obj_in={"bal": super_user_bal},
            )
            user = await crud.user.get(db=db, entity_id=owner_id)
            user_bal = user["bal"]
            if "bal" in user and currency.lower() in user["bal"]:
                user_bal[currency.lower()] = Decimal(
                    str(user["bal"][currency.lower()])
                ) - (Decimal(str(amount)) + Decimal(str(fee)))
            else:
                user_bal[currency.lower()] = user["bal"][currency.lower()] - (
                    Decimal(str(amount)) + Decimal(str(fee))
                )

            await crud.user.update(
                db=db, db_obj={"id": owner_id}, obj_in={"bal": user_bal}
            )

        except ValueError as e:
            print("Exception in outgoing transaction", e.args[0])
    return


async def test():
    user = await crud.user.get_by_email(db=db, email="dg@fastapi.xyz")
    user_bal = {"bal": {"usdt": 20}}
    await crud.user.update(db=db, db_obj=user, obj_in=user_bal)


if __name__ == "__main__":
    asyncio.run(incoming_transaction())
    asyncio.run(outgoing_transaction())
    asyncio.run(send_callback())
    asyncio.run(exchange())
    asyncio.run(send_callback())
    asyncio.run(fill_transaction())
    # asyncio.run(test())
