import anyio
from trade.db.session import database as db
import smtplib
import ssl


async def main():
    aggregation = [{"$match": {"to_coin": "USDT"}}]
    total = 0
    async for pair in db.exchange_mecx.aggregate(aggregation):
        total += 1

    port = 465  # For SSL
    smtp_server = "mongo.one"
    sender_email = "dg@mongo.one"  # Enter your address
    receiver_email = "dmitriy.golub@gmail.com"  # Enter receiver address
    password = "T3ip2ocean"
    message = f"""\
    Subject: Total records

    USDT{total}"""

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
    anyio.run(main)
