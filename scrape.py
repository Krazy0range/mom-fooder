from mom_fooder.database import Database

database = Database("mom_fooder/database/testing_database.json")
database.scrape_products()
