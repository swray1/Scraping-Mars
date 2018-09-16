from flask import Flask, render_template, redirect
from flask_pymongo import MongoClient, PyMongo
from scrape_mars import scrape
import pymongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars = mongo.mars.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def get():
    mars = mongo.mars
    data = scrape()
    mars.update({}, data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()
