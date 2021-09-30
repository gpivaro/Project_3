import os
import pandas as pd
import datetime
import psycopg2
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pickle
from Get_IP import get_client_ip

###############################################
# Flask Setup
###############################################
app = Flask(__name__)

###############################################
# Database
###############################################

# Database name and database tables
database_name = "project3database"

# Verify if there is a environment variable with the DATABASE_URL.
# Otherwise use the credentials from the api_keys file
try:
    db_uri = os.environ["DATABASE_URL"]
except KeyError:
    # from api_keys import DATABASE_URL
    # db_uri = DATABASE_URL

    from api_keys import mysql_user_project_3, mysql_pass_project_3, mysql_hostname, mysql_port
    db_uri = f"mysql+mysqlconnector://{mysql_user_project_3}:{mysql_pass_project_3}@{mysql_hostname}:{mysql_port}/{database_name}"

# print(db_uri)
    
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Create class to frame each real state instance
class RealState(db.Model):
    __tablename__ = "realstatelisting"

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
        return "<Listing %r>" % (self.address)


# Create class to frame each real state instance
class UserSelection(db.Model):
    __tablename__ = "userselection"

    userselection_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300))
    useremail = db.Column(db.String(300))
    house_id = db.Column(db.Integer, db.ForeignKey("realstatelisting.house_id"))
    user_choice = db.Column(db.String(300))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Listing %r>" % (self.userselection_id)


class VisitorInfo(db.Model):
    __tablename__ = "visitoripinfo"
    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.String(300), nullable=True)
    country = db.Column(db.String(300), nullable=True)
    region = db.Column(db.String(300), nullable=True)
    city = db.Column(db.String(300), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)


###############################################
# Machine Learning Model
###############################################
def load_model():
    global model
    with open(os.path.join("static", "Models", "kmeans1.pkl"), "rb") as f:
        model = pickle.load(f)
        print("model loaded")


###############################################
# Routes
###############################################

# Recreate database each time for demo
# Running these lines will erase all the data on the db
@app.before_first_request
def setup():
    load_model()
    # db.drop_all()
    # db.create_all()


# Home page / index page
@app.route("/", methods=["GET", "POST"])
def index():

    # get visitor ip address info
    response = get_client_ip(request)
    # Save visitor ip to database
    visitorinfo = VisitorInfo(
        ipaddress=response["ip"],
        country=response["location"]["country"],
        region=response["location"]["region"],
        city=response["location"]["city"],
        latitude=response["location"]["lat"],
        longitude=response["location"]["lng"],
    )
    # Skip saving if on local host
    if response["ip"] != "127.0.0.1":
        db.session.add(visitorinfo)
        db.session.commit()

    if request.method == "POST":

        user = request.form["fname"]

        return redirect(f"/classify/{user}")

    return render_template("index.html")


# Return all the routes available
@app.route("/routes")
def routes_available():

    return render_template("routes.html")


# Page for user classification of the real state
@app.route("/classify/<string:user>", methods=["GET", "POST"])
def classify(user):
    """ https://www.youtube.com/watch?v=_sgVt16Q4O4 """
    if request.method == "POST":
        print(f"User: {request.form['username']}")
        print(f"House ID: {request.form['houseID']}")
        print(f"User selection: {request.form.getlist('myCheckbox')}")
        userchoice = UserSelection(
            username=request.form["username"],
            house_id=request.form["houseID"],
            user_choice=request.form["myCheckbox"],
        )

        db.session.add(userchoice)
        db.session.commit()

        return redirect(f"/classify/{user}")

    return render_template("classify.html", myVar=user)


# API to access all houses on the database
@app.route("/api/realstatelistings")
def realstatelistings():

    # Retrieve data from database
    listings = (
        db.session.query(
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
            RealState.created_date,
        )
        .filter(RealState.latitude.isnot(None))
        .order_by(RealState.house_id)
        .all()
    )

    # Convert the data to a dataframe
    listing_df = pd.DataFrame(listings)

    # Fill NaN so JS can handle it
    listing_df = listing_df.fillna(0)

    # Run Kmeans clustering model
    predicted_clusters = model.predict(
        listing_df[["latitude", "longitude", "price"]].values
    )
    listing_df["cluster"] = predicted_clusters

    # Convert dataframe to dictionary
    listing_dict = listing_df.to_dict(orient="records")

    # Return json version of the data
    return jsonify(listing_dict)


# API to access the user selections
@app.route("/api/userselections/<string:UserName>")
def userselections(UserName):

    # Retrieve data from database
    userchoices = (
        db.session.query(
            UserSelection.userselection_id,
            UserSelection.username,
            UserSelection.useremail,
            UserSelection.house_id,
            UserSelection.user_choice,
            UserSelection.created_date,
        )
        .filter_by(username=UserName)
        .order_by(UserSelection.created_date)
    )

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

    return (
        f"""<h4>Thanks.</h4>
            <p>You have made your selection for all the houses that we have available at this moment. <br>
            We will see you soon with more houses.</p>"""
        f"<html><a href='/'>Home</a></html>"
    )


# Route to suggest houses based on the cluster and the previous user selection
@app.route("/api/house-cluster/<string:houseID>")
def house_cluster(houseID):

    # Retrieve data from database
    house = (
        db.session.query(
            RealState.house_id, RealState.price, RealState.latitude, RealState.longitude
        )
        .filter(RealState.house_id == houseID)
        .first()
    )

    # Apply the model on the house selected
    house_cluster = int(
        model.predict([[house.latitude, house.longitude, house.price]])[0]
    )

    return jsonify({"house_id": houseID, "house_cluster": house_cluster})


# API to access the visitors info
@app.route("/api/show-visitors/<string:type>/")
def show_visitors(type):

    if type == "all":
        visitorinfo = db.session.query(
            VisitorInfo.ipaddress,
            VisitorInfo.country,
            VisitorInfo.region,
            VisitorInfo.city,
            VisitorInfo.latitude,
            VisitorInfo.longitude,
        )

        # Convert the data to a dataframe
        visitorinfo_df = pd.DataFrame(visitorinfo)
        # Convert dataframe to dictionary
        visitorinfo_dict = visitorinfo_df.to_dict(orient="records")

    elif type == "count":
        visitorcount = db.session.query(VisitorInfo.id).count()

        visitorinfo_dict = {"visitors": visitorcount}

    # Return json version of the data
    return jsonify(visitorinfo_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)

