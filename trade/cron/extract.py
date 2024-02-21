from data import data

print("coins = (")
for coin in data:
    text = "".join(['"', coin["coin"], '",'])
    print(text)
print(")")
