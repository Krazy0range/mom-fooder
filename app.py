from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    headers = {"User-Agent": "Mozilla/5.0"}
    request = requests.get("https://www.costco.com", headers=headers)
    data = request.text
    return render_template("index.html", data=data)
