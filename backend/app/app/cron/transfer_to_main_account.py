from app.services.client import OKX
import time

sub_accounts = ["OPtvwZUK", "OPksiZLG", "OPhhgEFB", "OPsvbMDS", "OPgojJXH"]

if __name__ == "__main__":
    for sub_account in sub_accounts:
        okx = OKX()
        sub_account_api_keys = okx.create_sub_account_api_key(sub_account)
        time.sleep(2)
        if len(sub_account_api_keys["data"]) == 0:
            print("No api keys", sub_account_api_keys)
        else:
            sub_account_balance = okx.get_sub_account_balance(sub_account=sub_account)
            time.sleep(2)
            currency = sub_account_balance["data"][0]["ccy"]
            amount = sub_account_balance["data"][0]["bal"]
            print("Currency Amount Sub Account", currency, amount, sub_account)
            if float(sub_account_balance["data"][0]["bal"]) > 0:
                balance = okx.transfer_money_to_main_account(
                    ccy=currency,
                    amt=amount,
                    sub_account=sub_account,
                )
                print(balance)
