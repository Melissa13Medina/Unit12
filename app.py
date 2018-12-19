from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    red_planet= mongo.db.red_planet.find_one()
    return render_template("index.html", red_planet=red_planet)


@app.route("/scrape")
def scraper():
    red_planet = mongo.db.red_planet
    scrape_data = scrape_mars.scrape()
    red_planet.update({}, scrape_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)