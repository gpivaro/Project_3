from scrapy_realstate import scraped_data
from address_cordinates import get_coordinates
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
from sqlalchemy import exc

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
    address = db.Column(db.String(300))
    house_link = db.Column(db.String(300))
    photolink = db.Column(db.String(300))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return '<Listing %r>' % (self.address)


@app.route("/")
def home():

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

#     listings = [{'Price': 300000,
#   'Address': '13414 Boca Raton Dr, Houston, TX 77069',
#   'Link': 'https://www.realtor.com/realestateandhomes-detail/13414-Boca-Raton-Dr_Houston_TX_77069_M85440-60130',
#   'Photo link': ''},{'Price': 299999,
#   'Address': '4711 Hershe St, Houston, TX 77020',
#   'Link': 'https://www.realtor.com/realestateandhomes-detail/4711-Hershe-St_Houston_TX_77020_M92791-49875',
#   'Photo link': ''}]
    
    n = 0
    for item in listings:

        price = int(item["Price"])
        address = item["Address"]
        house_link = item["Link"]
        photolink = item["Photo link"]
        
        # get coordinates
        coordinates = get_coordinates(address)
        if coordinates:
            latitude = coordinates['latitude']
            longitude = coordinates['longitude']

        # Create an instance with the data if the coordinates are not empty
            house = RealState(
                price = price,
                address = address,
                house_link = house_link,
                photolink = photolink,
                latitude = latitude,
                longitude = longitude
                )
        else:
            house = RealState(
                price = price,
                address = address,
                house_link = house_link,
                photolink = photolink
                )

        

        # Add recordes to database
        try:
            db.session.add(house)
            db.session.commit()
            n = n + 1
        
        # To handle the duplicated entry
        except exc.IntegrityError:
            db.session.rollback()
            print('Duplicated Entry')
           

    # return redirect("/", code=302)
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
        RealState.longitude
        ).all()

    # Convert the data to a dataframe
    listing_df = pd.DataFrame(listings)
    
    # Convert dataframe to dictionary
    listing_dict = listing_df.to_dict(orient="records")

    # Return json version of the data
    return jsonify(listing_dict)

if __name__ == "__main__":
    app.run(debug=True)


