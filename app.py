import os
import pandas as pd
import datetime
import psycopg2
from flask import (Flask,render_template,jsonify,request,redirect, url_for)
from flask_sqlalchemy import SQLAlchemy



###############################################
# Flask Setup
###############################################
app = Flask(__name__)

###############################################
# Database
###############################################

# Verify if there is a environment variable with the DATABASE_URL.
# Otherwise use the credentials from the api_keys file
try:
    db_uri = os.environ['DATABASE_URL']
except KeyError:
    from api_keys import DATABASE_URL
    db_uri = DATABASE_URL

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
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

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
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    

    def __repr__(self):
        return '<Listing %r>' % (self.userselection_id)


###############################################
# Routes
###############################################


# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     db.drop_all()
#     db.create_all()


# Home page / index page
@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
            
        user = request.form['fname']
        
        return redirect( f"/classify/{user}")

    return render_template("index.html")


# Return all the routes available
@app.route("/routes")
def routes_available():

    return render_template("routes.html")


# Page for user classification of the real state
@app.route("/classify/<string:user>", methods=['GET', 'POST'])
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


# API to access all houses on the database
@app.route("/api/realstatelistings")
def realstatelistings():

    # Retrieve data from database
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
                                RealState.google_map,
                                RealState.created_date
    ).filter(RealState.latitude.isnot(None)).order_by(RealState.house_id).all()
        
    # Convert the data to a dataframe
    listing_df = pd.DataFrame(listings)

    # Fill NaN so JS can handle it
    listing_df = listing_df.fillna(0)
    
    # Convert dataframe to dictionary
    listing_dict = listing_df.to_dict(orient="records")

    # Return json version of the data
    return jsonify(listing_dict)


# API to access the user selections
@app.route("/api/userselections/<string:UserName>")
def userselections(UserName):

    # Retrieve data from database
    userchoices = db.session.query(
                                    UserSelection.userselection_id,
                                    UserSelection.username,
                                    UserSelection.useremail,
                                    UserSelection.house_id,
                                    UserSelection.user_choice,
                                    UserSelection.created_date
                                ).filter_by(username = UserName)

    # Convert the data to a dataframe
    userchoices_df = pd.DataFrame(userchoices)

    # Try outer join
    # db.session.query(RealState,UserSelection).outerjoin(UserSelection,RealState.house_id == UserSelection.house_id).filter_by(username = 'Gabriel').all()
    
    # Convert dataframe to dictionary
    userchoices_dict = userchoices_df.to_dict(orient="records")

    # Return json version of the data
    return jsonify(userchoices_dict)


# Real state map and general info
@app.route("/analysis")
def analysis():

    return render_template("analysis.html")

# Real state map
@app.route("/map")
def map_view():

    return render_template("map.html")


# Route when the user's has no more houses to select
@app.route("/end-classification")
def end_classification():
        
    return (f"""<h4>Thanks.</h4>
            <p>You have made your selection for all the houses that we have available at this moment. <br>
            We will see you soon with more houses.</p>"""
            f"<html><a href='/'>Home</a></html>")



if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5100, debug=True)


