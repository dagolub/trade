from trade.db.session import database as db

with open('/home/dg/Downloads/proxy_http_auth.txt') as f:
    lines = f.readlines()

for line in lines:
    host, port = line.strip().split(":")
    print(host, port)
    db["proxy"].insert_one({"host": host, "port": port})