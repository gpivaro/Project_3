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
    from api_keys import DATABASE_URL
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
    # db_uri = f"postgresql://{pgadim_user}:{pgadim_pass}@localhost:5432/project3_db"
    db_uri = DATABASE_URL
    
    print(db_uri)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create class to frame each real state instance
class RealState(db.Model):
    __tablename__ = 'realstatelisting'

    house_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    bed = db.Column(db.Float, nullable=True)
    bath = db.Column(db.Float, nullable=True)
    sqft = db.Column(db.Float, nullable=True)
    lot = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    house_link = db.Column(db.String(300), nullable=True)
    image_1 = db.Column(db.String(300), nullable=True)
    image_2 = db.Column(db.String(300), nullable=True)
    map_link = db.Column(db.String(300), nullable=True)
    google_map = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return '<Listing %r>' % (self.address)

# Create class to frame each real state instance
class UserSelection(db.Model):
    __tablename__ = 'userselection'

    userselection_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300))
    useremail = db.Column(db.String(300))
    house_id = db.Column(db.Integer, db.ForeignKey('realstatelisting.house_id'))
    user_choice = db.Column(db.String(300))
    

    def __repr__(self):
        return '<Listing %r>' % (self.userselection_id)

# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     db.drop_all()
#     db.create_all()

# Home page
@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
            
        user = request.form['fname']
        
        return redirect( f"/classify/{user}")

    return render_template("index.html")

@app.route("/routes")
def routes_available():

    return (
        f"<h4>Routes:</h4>"
        f"<p>/classify/user</p>"
        f"<p>/api/realstatelistings/queryfilter</p>"
        f"<p>/scrapy/page_number</p>"
        f"<p>/api/userselections/UserName</p>"
        f"<html><a href='/'>Home</a></html>"
        )

@app.route("/classify/<user>", methods=['GET', 'POST'])
def classify(user):
    """ https://www.youtube.com/watch?v=_sgVt16Q4O4 """
    if request.method == 'POST':
        print(f"User: {request.form['username']}")
        print(f"House ID: {request.form['houseID']}")        
        print(f"User selection: {request.form.getlist('myCheckbox')}")
        userchoice = UserSelection(
            username = request.form['username'],
            house_id = request.form['houseID'], 
            user_choice = request.form['myCheckbox']
            )
        
        db.session.add(userchoice)
        db.session.commit()

        return redirect( f"/classify/{user}")
    
    return render_template("classify.html", myVar=user)


# # Scrapy the data
# @app.route("/scrapy/<page_number>")
# def scrapy(page_number):

#     # run function to scrapy data
#     listings = scraped_data(page_number)

#     # add new records to database
#     # new_records = addtodatabase(listings, RealState, db)

#     n = 0
#     for item in listings:
#         result = addonetodatabase(item, RealState, db)
#         if result == True:
#             n = n + 1

#     return (f"New recordes added to database: {n}<br>"
#             f"<html><p><a href='/'>Home</a></p></html>"
#             )


# API to access all houses on the database
@app.route("/api/realstatelistings/<string:query_string>")
def realstatelistings(query_string):

    if query_string == 'photo':
        # Retrieve data from database excluding the entries with no photo and no coordinates
        listings = db.session.query(
                                    RealState.house_id,
                                    RealState.address,
                                    RealState.price,
                                    RealState.bed,
                                    RealState.bath,
                                    RealState.sqft,
                                    RealState.lot,
                                    RealState.latitude,
                                    RealState.longitude,
                                    RealState.house_link,
                                    RealState.image_1,
                                    RealState.image_2,
                                    RealState.map_link,
                                    RealState.google_map
        ).filter(RealState.latitude.isnot(None)).filter(RealState.image_1 != "").all()
    else:
        # Retrieve data from database excluding the entries with no photo and no coordinates
        listings = db.session.query(RealState.house_id,
                                    RealState.address,
                                    RealState.price,
                                    RealState.bed,
                                    RealState.bath,
                                    RealState.sqft,
                                    RealState.lot,
                                    RealState.latitude,
                                    RealState.longitude,
                                    RealState.house_link,
                                    RealState.image_1,
                                    RealState.image_2,
                                    RealState.map_link,
                                    RealState.google_map).filter(RealState.latitude.isnot(None)).all()
            
    # Convert the data to a dataframe
    listing_df = pd.DataFrame(listings)

    # Fill NaN so JS can handle it
    listing_df = listing_df.fillna(0)
    
    # Convert dataframe to dictionary
    listing_dict = listing_df.to_dict(orient="records")

    # Return json version of the data
    return jsonify(listing_dict)


# API to access the user selections
@app.route("/api/userselections/<UserName>")
def userselections(UserName):

    # Retrieve data from database
    userchoices = db.session.query(
                                    UserSelection.userselection_id,
                                    UserSelection.username,
                                    UserSelection.useremail,
                                    UserSelection.house_id,
                                    UserSelection.user_choice
                                ).filter_by(username = UserName)

    # Convert the data to a dataframe
    userchoices_df = pd.DataFrame(userchoices)
    
    # Convert dataframe to dictionary
    userchoices_dict = userchoices_df.to_dict(orient="records")

    # Return json version of the data
    return jsonify(userchoices_dict)

# Real state map
@app.route("/realstate")
def realstate():

    return render_template("realstate.html")


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5100, debug=True)


