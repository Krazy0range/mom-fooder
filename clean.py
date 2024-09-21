import json


def clean_price(price):
    if type(price) is float:
        return price
    price = price.replace("$", "")
    price = price.replace(",", "")
    price = price.replace(" ", "")
    try:
        i = price.find(next(filter(str.isalpha, price)))
    except StopIteration:
        i = -1
    price = price[0:i]
    return float(price)


file_path = "mom_fooder/database/production_database.json"

data = []

with open(file_path, "r") as file:
    data = json.load(file)

for product in data:
    product["price"] = clean_price(product["price"])

with open(file_path, "w") as file:
    json.dump(data, file)
