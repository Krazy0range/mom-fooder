import json

from scraper import Scraper


class Database:

    def __init__(self):
        self.scraper = Scraper()

        self.costco_products = None

        self.load_costco()

    def load_costco(self):
        with open("costco.json", "r") as f:
            self.costco_products = json.load(f)

    def index_costco(self):
        self.scraper.scrape_costco()
        self.costco_products = self.scraper.costco_products

        with open("costco.json", "w") as f:
            json.dump(self.costco_products, f)
