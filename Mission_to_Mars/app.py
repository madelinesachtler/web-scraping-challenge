
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2
import time 
# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    ### --- NEED THIS TO IMPORT INTO HTML --- ## 
    
    mars = mongo.db.mars.find_one()
    print(mars)
    # Return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars = mongo.db.mars
    mars_data = scrape_mars2.scrape_info()

    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
