from flask import Flask, render_template

from scraper import Scraper

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    scraper = Scraper()
    scraper.scrape_costco()
    return render_template("index.html", products=scraper.costco_scraps)
