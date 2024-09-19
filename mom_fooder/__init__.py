import flask

from mom_fooder.database import Database


def create_app():

    app = flask.Flask(__name__, template_folder="../templates", static_folder="../static")

    database = Database("mom_fooder/database/production_database.json")

    @app.route("/")
    def index():
        return flask.render_template("index.html", products=database.products)

    return app
