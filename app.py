from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape():

    # Run scrape functions
    mars_dict = scrape_mars.scrape_sites()

    # Store results into a dictionary

    mars_dict = {
        "news_title": mars_dict["news_title"],
        "news_p": mars_dict["news_p"],
        "featured_image_url": mars_dict["featured_image_url"],
        "mars_weather": mars_dict["mars_weather"],
        "mars_facts": mars_dict["mars_facts"],
        "hemisphere_image_urls": mars_dict["hemisphere_image_urls"],
    }

    # Drop existing data from database
    mongo.db.collection.drop()

    # Insert mars_update into database
    mongo.db.collection.insert_one(mars_dict)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)