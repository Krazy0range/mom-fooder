import json


def clean_price(price):
    chars = "foreachs$- "
    for char in chars:
        price = price.replace(char, "")
    return price


file_path = "mom_fooder/database/production_database.json"

data = []

with open(file_path, "r") as file:
    data = json.load(file)

for product in data:
    product["price"] = clean_price(product["price"])

with open(file_path, "w") as file:
    json.dump(data, file)
