# Imports
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars      

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

client = MongoClient("localhost", 27017)
db = client["mars_db"]
collection = db["mars"] 

# mars_dict = scrape_mars.scrape()
# collection.insert_one(mars_dict)

# Root route
@app.route("/")
def index():
    # find one document from the mongo db and return it.
    mars = mongo.db.mars.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars=mars)

# Run Scrape function
@app.route("/scrape")
def scraper():
    # create a mars database
    mars = mongo.db.mars
    # call the scrape function in the scrape_mars file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()
    # update the mars data with the data that is being scraped.
    mars.replace_one({}, mars_data, upsert=True)
    # return a message to the page so we know it was successful.
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)