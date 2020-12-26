from scrapy_realstate import scraped_data
from database_scripts import addonetodatabase

import os
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect
)
from flask_sqlalchemy import SQLAlchemy
import psycopg2

try:
    # Import DB user and password
    from api_keys import pgadim_user
    from api_keys import pgadim_pass
except:
    pass


###############################################
# Flask Setup
###############################################
app = Flask(__name__)

###############################################
# Database
###############################################

try:
    db_uri = os.environ['DATABASE_URL']
except KeyError:
    db_uri = f"postgresql://{pgadim_user}:{pgadim_pass}@localhost:5432/project3_db"
    print(db_uri)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

# Create class to frame each real state instance
class RealState(db.Model):
    __tablename__ = 'realstatelisting'

    house_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    address = db.Column(db.String(300), unique=True, nullable=False)
    house_link = db.Column(db.String(300))
    photolink = db.Column(db.String(300))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    map_link = db.Column(db.String(300))

    def __repr__(self):
        return '<Listing %r>' % (self.address)

# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     db.drop_all()
#     db.create_all()


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/routes")
def routes_available():

    return (
        f"<h3>Welcome</h3><br>"
        f"<h4>Routes:</h4>"
        f"<p>/scrapy/page_number</p>"
        f"<p>/api/realstatelistings</p>"
        )

@app.route("/scrapy/<page_number>")
def scrapy(page_number):

    # run function to scrapy data
    listings = scraped_data(page_number)

    # add new records to database
    # new_records = addtodatabase(listings, RealState, db)

    n = 0
    for item in listings:
        result = addonetodatabase(item, RealState, db)
        if result == True:
            n = n + 1

    return f"New recordes added to database: {n}"



@app.route("/api/realstatelistings")
def realstatelistings():

    # Retrieve data from database
    listings = db.session.query(
        RealState.house_id, 
        RealState.price, 
        RealState.address, 
        RealState.house_link,
        RealState.photolink,
        RealState.latitude,
        RealState.longitude,
        RealState.map_link
        ).all()

    # Convert the data to a dataframe
    listing_df = pd.DataFrame(listings)
    
    # Convert dataframe to dictionary
    listing_dict = listing_df.to_dict(orient="records")

    # Return json version of the data
    return jsonify(listing_dict)

if __name__ == "__main__":
    app.run(debug=True)


