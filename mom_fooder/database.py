import json
from mom_fooder.scraper import Scraper


class Database:

    def __init__(self, database_file):
        self.database_file = database_file
        self.scraper = Scraper()

        self.products = []

        self.load_products()

    def scrape_products(self):
        self.heb_products = self.scraper.scrape_heb()
        for product in self.heb_products:
            self.products.append(product)
        self.dump_products()

    def load_products(self):
        with open(self.database_file, "r") as f:
            self.products = json.load(f)

    def dump_products(self):
        with open(self.database_file, "w") as f:
            self._remove_duplicate_products()
            json.dump(self.products, f)

    def _remove_duplicate_products(self):
        self.products = list({v["name"]: v for v in self.products}.values())
