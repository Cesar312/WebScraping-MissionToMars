import pymongo
from flask import Flask, render_template, redirect
import scrape_mars

app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_app
db.mars_data.drop()
collection = db.mars_data

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    destination = collection.find_one()

    return render_template("index.html", mars=destination)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = collection
    mars_results = scrape_mars.scraper()
    mars.update({}, mars_results, upsert=True)
    
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
