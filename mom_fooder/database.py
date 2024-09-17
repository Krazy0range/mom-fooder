import json
from mom_fooder.scraper import Scraper


class Database:

    def __init__(self, database_file):
        self.database_file = database_file
        self.scraper = Scraper()

        self.products = []

        self.load_products()

    def scrape_products(self):
        # self.costco_products = self.scraper.scrape_costco()
        self.costco_products = []
        self.heb_products = self.scraper.scrape_heb()

        self.products = self.costco_products + self.heb_products
        self.dump_products()

    def load_products(self):
        with open(self.database_file, "r") as f:
            self.products = json.load(f)

    def dump_products(self):
        with open(self.database_file, "w") as f:
            json.dump(self.products, f)
