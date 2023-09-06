import asyncio
from app.services.okx_client import OKX
from app.core.config import settings

sub_accounts = [
    "postertsknb",
    "Userjmgav",
    # "OleskBackendhfxDDL",
    # "OleskBackendwxrmg",
]

if __name__ == "__main__":
    for sub_account in sub_accounts:
        okx = OKX()
        api = okx.get_sub_account_api_key(sub_account, settings.OKX_API_KEY)

        sub_account_balance = okx.get_account_balance(
            "USDT", api_key, secret_key, passphrase
        )
        # if float(sub_account_balance["data"][0]["bal"]) > 0:
        #     balance = okx.transfer_money_to_main_account(
        #         ccy=sub_account_balance["data"][0]["ccy"],
        #         amt=sub_account_balance["data"][0]["bal"],
        #         sub_account=sub_account,
        #     )
        #     sleep(2)
