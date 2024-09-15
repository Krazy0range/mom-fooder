from flask import Flask, render_template

from database import Database

app = Flask(__name__, template_folder="templates")

database = Database()


@app.route("/")
def index():
    return render_template("index.html", products=database.costco_products)
