

### Import Dependencies
import os
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time
import numpy as np
import pprint
import datetime

 # Imports the method used to connect to DBs
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import update
# Imports the methods needed to abstract python classes into database tables
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# function to establish a session with a connected database
from sqlalchemy.orm import Session
# database compliant datatypes
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime


# Import DB user and password
from api_keys import positionstack_key
from api_keys import opencagedata_API
from api_keys import DATABASE_URL

def get_coordinates():
    ### Setup Splinter (For Mac)
    # identify location of chromedriver and store it as a variable
    # driverPath = !which chromedriver
    driverPath = ["/usr/local/bin/chromedriver"]  # For MacBook

    # Setup configuration variables to enable Splinter to interact with browser
    executable_path = {"executable_path": driverPath[0]}
    browser = Browser('chrome', **executable_path, headless=False)

    ## Save Scraped House Data to Database
    # Create database connection
    engine = create_engine(DATABASE_URL) 

    # Create class to frame each real state instance
    class RealState(Base):
        __tablename__ = 'realstatelisting'

        house_id = Column(Integer, primary_key=True)
        address = Column(String(300), unique=True, nullable=False)
        price = Column(Float, nullable=False)
        bed = Column(Float, nullable=True)
        bath = Column(Float, nullable=True)
        sqft = Column(Float, nullable=True)
        lot = Column(Float, nullable=True)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        house_link = Column(String(300), nullable=True)
        image_1 = Column(String(300), nullable=True)
        image_2 = Column(String(300), nullable=True)
        map_link = Column(String(300), nullable=True)
        google_map = Column(String(300), nullable=True)
        created_date = Column(DateTime, default=datetime.datetime.utcnow)

        def __repr__(self):
            return '<Listing %r>' % (self.address)

            # Create class to frame each real state instance
    class UserSelection(Base):
        __tablename__ = 'userselection'

        userselection_id = Column(Integer, primary_key=True)
        username = Column(String(300))
        useremail = Column(String(300))
        house_id = Column(Integer, ForeignKey('realstatelisting.house_id'))
        user_choice = Column(String(300))
        created_date = Column(DateTime, default=datetime.datetime.utcnow)
        
        def __repr__(self):
            return '<Listing %r>' % (self.userselection_id)


    # Create all of the tables in our database based on the classes we've associated with our declarative base.
    Base.metadata.create_all(engine)

    # Create a Session object to connect to DB
    session = Session(bind=engine)


    ### Get Coordinates Using Google Maps
    """ Get house coordinates using Splinter to scrap Google Maps """
    def find_coordinates(url):
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        time.sleep(5)
        current_url = browser.url
        browser.quit()

        try:
            latitude = float(current_url.split("!")[-2].split("d")[1])
            longitude = float(current_url.split("!")[-1].split("d")[1])
        except IndexError:
            url_string_list = current_url.split("/")
            for jj in range(len(url_string_list)):
                try:
                    index_coordinates = url_string_list[jj].index("@")
                except ValueError:
                    pass
                else:
                    latitude = float(url_string_list[jj][1:-1].split(",")[0])
                    longitude = float(url_string_list[jj][1:-1].split(",")[1])
            
        map_link = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}"

        return {"latitude":latitude, "longitude":longitude, "map_link": map_link}


    """ Query houses and update entry with coordinates and map link """
    def update_house_coordinates(HouseID):
        house = session.query(RealState).filter(RealState.house_id == HouseID)
        coordinates = find_coordinates(house[0].google_map)
        stmt = update(RealState).where(RealState.house_id == HouseID).values(coordinates).\
            execution_options(synchronize_session="fetch")

        session.execute(stmt)
        session.commit()

    # Update coordinates for all entries of the database that doesn't have coordinates
    house_list = session.query(RealState).filter(RealState.latitude == None).order_by(RealState.house_id).all()
    nn = 0
    for house in house_list:
        update_house_coordinates(house.house_id)
        nn = nn + 1

    print(f"--> {nn} records updated.")

    

    ### Query database
    # Query all records and create a list with the returned data
    query_result = session.query(RealState).all()
    print('')
    print(f"Current records on database: {len(query_result)}.")

    session.close()



get_coordinates()