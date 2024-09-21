import requests
import traceback
from bs4 import BeautifulSoup

import asyncio
import nodriver as nodriver


class Scraper:

    def __init__(self):
        pass

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

        return products

    def scrape_costco_page(self, url):
        print(f"scraping {url}")
        headers = {"User-Agent": "Mozilla/5.0"}
        request = requests.get(url, headers=headers)
        soup = BeautifulSoup(request.text, "html.parser")
        soup_products = [tag for tag in soup.find_all("div", class_="product-tile-set")]
        products = []
        for soup_product in soup_products:
            product = {}
            try:
                product["price"] = soup_product.find("div", class_="price").text.strip()
            except AttributeError:
                continue
            product["name"] = soup_product.find("img").get("alt")
            product["store"] = "Costco"
            product["url"] = soup_product.find("a", class_="product-image-url")["href"]
            products.append(product)
        try:
            soup_next_page_url = soup.select_one("li.forward > a")["href"]
        except TypeError:
            pass
        else:
            next_page_products = self.scrape_costco_page(soup_next_page_url)
            products = products + next_page_products
        return products

    def scrape_heb(self):
        return asyncio.run(self.scrape_heb_())

    async def scrape_heb_(self):
        heb_category_pages = [
            "https://www.heb.com/category/shop/fruit-vegetables/2863/490020",
            "https://www.heb.com/category/shop/meat-seafood/2863/490023",
            "https://www.heb.com/category/shop/bakery-bread/2863/490014",
            "https://www.heb.com/category/shop/dairy-eggs/2863/490016",
            "https://www.heb.com/category/shop/deli-prepared-food/2863/490017",
            "https://www.heb.com/category/shop/pantry/2863/490024",
            "https://www.heb.com/category/shop/frozen-food/2863/490019",
            "https://www.heb.com/category/shop/beverages/2863/490015",
            "https://www.heb.com/category/shop/everyday-essentials/2863/490018",
            "https://www.heb.com/category/shop/health-beauty/2863/490021",
            "https://www.heb.com/category/shop/home-outdoor/2863/490022",
            "https://www.heb.com/category/shop/baby-kids/2863/489924",
            "https://www.heb.com/category/shop/pets/2863/490025",
            "https://www.heb.com/category/shop/donations/2863/1157212",
        ]
        products = []
        driver = await nodriver.start()
        for page in heb_category_pages:
            try:
                page_products = await self.scrape_heb_page(driver, page)
            except Exception:
                print(traceback.format_exc())
                print("exiting nicely, saving products for u")
                return products
            else:
                products += page_products
        return products

    async def scrape_heb_page(self, driver: nodriver.Tab, url):
        print(f"scraping {url}")
        page = await driver.get(url)
        await page.wait_for(selector=".sc-6fe35e2a-25")
        soup = BeautifulSoup(await page.get_content(), "html.parser")
        soup_products = [
            tag
            for tag in soup.find_all(
                "div",
                class_="sc-d9ba1e96-2 gySwXG sc-6cde8841-0 kzenFx",
            )
        ]
        products = []
        for soup_product in soup_products:
            product = {}
            product["store"] = "HEB"
            product["price"] = soup_product.find("span", class_="sc-d5b5e439-0 jLVXqw").text
            product["name"] = soup_product.find("span", class_="sc-98cc3b00-1 kBHxUg").text
            product["url"] = (
                "https://www.heb.com"
                + soup_product.find("a", class_="sc-6ec66450-0 sc-d9ba1e96-24 sc-d9ba1e96-26 jRvnpE dgDxSG hQZwXn sc-6cde8841-0 kzenFx")["href"]
            )
            products.append(product)
        soup_next = soup.find("a", class_="sc-5e657bf5-0 sc-d751beb-0 sc-58b2267-3 NGmVv iKMudD jqcvLk")
        if soup_next:
            next_url = "https://www.heb.com" + soup_next["href"]
            products = products + await self.scrape_heb_page(driver, next_url)
        return products

    def scrape_walmart(self):
        return asyncio.run(self.scrape_walmart_())

    async def scrape_walmart_(self):
        walmart_pages = [
            "https://www.walmart.com/browse/food/shop-all-game-time-food/976759_1567409_3282877_6093905?povid=GlobalNav_rWeb_Grocery_Grocery_TailgatingFood"
        ]
        products = []
        driver = await nodriver.start()
        for page in walmart_pages:
            page_products = await self.scrape_walmart_page(driver, page)
            products += page_products
        return products

    async def scrape_walmart_page(self, driver, url):
        page = await driver.get(url)
        await page.wait_for(selector=".mb0")
        page_content = await page.get_content()
        soup = BeautifulSoup(page_content, "html.parser")
        soup_products = [tag for tag in soup.find_all("div", class_="mb0 ph0-xl pt0-xl bb b--near-white w-25 pb3-m ph1")]
        products = []
        for soup_product in soup_products:
            product = {}
            product["store"] = "Walmart"
            price_tag = soup_product.find("div", class_="mr1 mr2-xl b black lh-solid f5 f4-l")
            if not price_tag:
                price_tag = soup_product.find("div", class_="mr1 mr2-xl b black green lh-solid f5 f4-l")
            price_subtag = price_tag.find("span", class_="f2")
            product["price"] = price_subtag.text + "." + price_subtag.next_sibling.text
            product["name"] = soup_product.find("span", class_="normal dark-gray mb0 mt1 lh-title f6 f5-l lh-copy").text
            product["url"] = "https://www.walmart.com" + soup_product.find("a", class_="w-100 h-100 z-1 hide-sibling-opacity absolute")["href"]
            products.append(product)
        await page.close()
        return products
