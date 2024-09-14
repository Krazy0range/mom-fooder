import requests
import json
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self):
        self.costco_scraps = None

    def scrape(self):
        self.scrape_costco()

    def scrape_costco(self):
        costco_category_pages = [
            "https://www.costco.com/snacks.html",
            "https://www.costco.com/meat.html",
            "https://www.costco.com/paper-products-food-storage.html",
            "https://www.costco.com/beverages.html",
            "https://www.costco.com/candy.html",
            "https://www.costco.com/deli.html",
            "https://www.costco.com/coffee-sweeteners.html",
            "https://www.costco.com/laundry-supplies.html",
            "https://www.costco.com/prepared-food.html",
            "https://www.costco.com/health-beauty.html",
            "https://www.costco.com/kirkland-signature-groceries.html",
            "https://www.costco.com/breakfast.html",
            "https://www.costco.com/pantry.html",
            "https://www.costco.com/cakes-cookies.html",
            "https://www.costco.com/cheese.html",
            "https://www.costco.com/organic-groceries.html",
            "https://www.costco.com/household-cleaning.html",
            "https://www.costco.com/wine.html",
            "https://www.costco.com/household.html",
            "https://www.costco.com/gift-baskets.html",
            "https://www.costco.com/emergency-kits-supplies.html",
            "https://www.costco.com/floral.html",
            "https://www.costco.com/pet-supplies.html",
        ]
        products = []
        for page in costco_category_pages:
            page_products = self.scrape_costco_page(page)
            products = products + page_products

        self.costco_scraps = products

        with open("costco.json", "w") as f:
            json.dump(self.costco_scraps, f)

    def scrape_costco_page(self, url):
        print(f"scraping {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, "html.parser")
        soup_products = [tag for tag in soup.find_all("div", class_="product-tile-set")]
        products = []
        for soup_product in soup_products:
            product = {}
            product["name"] = soup_product.find("img").get("alt")
            try:
                product["price"] = soup_product.find("div", class_="price").text
            except AttributeError:
                continue
            products.append(product)
        try:
            soup_next_page_url = soup.select_one("li.forward > a")["href"]
        except TypeError:
            pass
        else:
            next_page_products = self.scrape_costco_page(soup_next_page_url)
            products = products + next_page_products
        return products


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape()
    print(scraper.scraps)
