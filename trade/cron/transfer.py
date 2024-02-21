from trade.services.okx_client import OKX


okx = OKX()
balance = okx.transfer_money_to_main_account(
    ccy="USDT",
    amt=1,
    sub_account="trader",
)