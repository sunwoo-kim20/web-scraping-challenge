from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Connect to Mongo database and create collection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.marsDB
mars_info = db.mars_mission


# Route to render index.html template
@app.route("/")
def home():

    # Get data from Mongo
    mars_data = db.mars_mission.find()
    print(mars_data)

    # Return template and data
    return render_template("index.html", mars_data=mars_data[0])


# Route to use scrape function
@app.route("/scrape")
def scrape():

    mars_data = scrape_mars.scrape_data()

    # Update Mongo database
    db.mars_mission.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
