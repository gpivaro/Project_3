"""
Scrapy the real state website and retrieve house listing of a target price and retrieve the info and save to database.
"""

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

def scrapy_real_state(page_number):
    ### Setup Splinter (For Mac)
    # identify location of chromedriver and store it as a variable
    # driverPath = !which chromedriver
    driverPath = ["/usr/local/bin/chromedriver"]  # For MacBook

    # Setup configuration variables to enable Splinter to interact with browser
    executable_path = {"executable_path": driverPath[0]}
    browser = Browser('chrome', **executable_path, headless=False)

    ### Scraping

    # URL of page to be scraped
    url_realtor = "https://www.realtor.com/realestateandhomes-search/Houston_TX/type-single-family-home/price-"
    link_details = "https://www.realtor.com"
    min_price = '150000'
    max_price = '350000'
    sort_by = '/sby-2' # Highest to lowest price
    sort_by = '/sby-6' # Newest listings
    # page_number = 10

    query_url = f"{url_realtor}{min_price}-{max_price}{sort_by}/pg-{page_number}"
    print(query_url)

    ### Splinter
    # Use the browser to visit the url
    browser.visit(query_url)
    # Wait for x seconds for error purpouses
    time.sleep(5)

    # Return the rendered page by the browser
    html_realtor = browser.html

    # Use beatifulsoup to scrap the page rendered by the browser
    soup = BeautifulSoup(html_realtor, 'html.parser')

    """
    Find all lis in order to find each house item.
    Then look for the class = "photo-wrap" to retrieve the unique id
    for each listing. Hover the mouse over the house to load the picture and
    finally get the picture link to save in the database
    """
    house_ads = soup.find_all('li')
    for kk in range(len(house_ads)):
        if house_ads[kk].find_all('div', class_= "photo-wrap"):
            div_tag = house_ads[kk].find('div', class_= "photo-wrap")
            browser.find_by_id(div_tag['id']).mouse_over()
            time.sleep(1)

    # Return the rendered page by the browser after loading all photos
    html_realtor = browser.html

    # Use beatifulsoup to scrap the page rendered by the browser
    soup = BeautifulSoup(html_realtor, 'html.parser')

    # Search for the div where the title is located
    results = soup.find_all('div', class_="card-box")
    # print(results[0].prettify())
    print(f"Total results: {len(results)}")

    # Find beds, baths, sqft and lot
    def find_features(house_feat_temp):
        list_features = []
        for jj in range(len(house_feat_temp)):
            list_features.append(house_feat_temp[jj].text)

        try:
            index_pos = list_features.index("bed")
        except ValueError:
            bed = 1.0
        else:
            bed = float(list_features[index_pos-1])

        try:
            index_pos = list_features.index("bath")
        except ValueError:
            bath = 1.0
        else:
            bath = float(list_features[index_pos-1].replace("+",""))

        try:
            index_pos = list_features.index("sqft")
        except ValueError:
            sqft = np.nan
        else:
            sqft = float(list_features[index_pos-1].replace(",",""))

        try:
            index_pos = list_features.index("sqft lot")
        except ValueError:
            try:
                index_pos = list_features.index("acre lot")
            except ValueError:
                lot = np.nan
            else:
                lot = round(float(list_features[index_pos-1])*43560)    
        else:
            lot = float(list_features[index_pos-1].replace(',',''))
    
        return {"Beds": bed, "Bath": bath, "Sqft": sqft, "Lot": lot}

    # find_features(results[6].find('ul').find_all('span'))


    # Main Funtction: Print results and save to a dictionary
    n = 0
    realstate_list = []
    for result in results:
    #     Clear the variables to not store repeated info
        house_price = ''
        address = ''
        link_page = ''
        photo_url = ''
                    
        n = n + 1
        print('-----------------------------------')
        print('')
        print(f'Result: {n} of {len(results)}')
        if not result.find('div', class_="ads"):

            price_div = result.find('div', class_="price")
            house_price = float(price_div.find('span').text.split('$')[-1].replace(",",""))
            link_page = result.find('a')['href']
            img_label = result.find('img')
            address = img_label['alt']
            
            features = find_features(result.find('ul').find_all('span'))
            
            bed = features['Beds']
            bath = features['Bath']
            sqft = features['Sqft']
            lot = features['Lot']
                
            print(f"Price: ${house_price} | Beds: {bed}, Bath: {bath}, Sqft: {sqft}, Lot: {lot}")        
            print(f"Address: {address}")
            
            try:
                price_reduced = result.find('span', class_="price-reduced-amount")
                price_now = price_reduced.text
                print(f"Price reduced: {price_now}")
            except:
                pass
            print(f"Link: {link_details}{link_page}")
        
            separator = '+'
            address_google = separator.join(address.split(" "))
            url_google_maps = f"https://www.google.com/maps/place/{address_google}"
            print(f"Google Maps: {url_google_maps}")
        
            list_images = ['', '']
            house_pictures_tag = result.find_all('picture')
            for uu in range(len(house_pictures_tag)):
                list_images[uu] = house_pictures_tag[uu].find('img')['srcset'].split(',')[1].split(' ')[1]
                print(f"Image_{uu}: {list_images[uu]}")
            
            # Save results to a dictionary
            realstate_list.append(
                {
                    "Price": house_price,
                    "Address": address,
                    "Beds": bed,
                    "Baths": bath,
                    "Sqft": sqft,
                    "Lot": lot,
                    "Image_1": list_images[0],
                    "Image_2": list_images[1],
                    "Link": str(link_details+link_page),
                    "Google Maps": url_google_maps
                }
            )

        
        else:
            print('Data not available or Ads')

        print('')

    # When you’ve finished testing, close your browser using browser.quit:
    browser.quit()


    ### Data Cleaning
    # Save the data to a dataframe
    listing_df = pd.DataFrame(realstate_list)
    # listing_df.to_csv(os.path.join('Database','ScrapedData.csv'))
    listing_df.head(2)

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


    """ Verify if the items are in the database to avoid roll back"""
    new_entries_index = []
    for nn in range(len(listing_df)):
        house_item = listing_df.iloc[nn]
        query_results = session.query(RealState).filter(RealState.address == house_item.Address).all()
        if query_results:
            pass
        else:
            new_entries_index.append(nn)

    new_houses_df = listing_df.iloc[new_entries_index]
    new_houses_df = new_houses_df.drop_duplicates()
    print(f"--> {len(new_houses_df)} records to be added.")


    ll = 0
    for nn in range(len(new_houses_df)):
    #     print('-'*25)
    #     print(f"{nn+1} of {len(listing_df)}")
        house_item = new_houses_df.iloc[nn]

        new_house = RealState(
            address = house_item.Address,
            price = house_item.Price,
            bed = house_item.Beds,
            bath = house_item.Baths,
            sqft = house_item.Sqft,
            lot = house_item.Lot,
            image_1 = house_item['Image_1'],
            image_2 = house_item['Image_2'],
            house_link = house_item.Link,
            google_map = house_item['Google Maps']
            )
        
        try:
            session.add(new_house)
            session.commit()
            ll = ll + 1
        except exc.IntegrityError:
            session.rollback()
            print(f'Roll back: {new_house}')

    print(f"--> Total recordes added to database: {ll}.")

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

    session.close()

    ### Query database
    # Query all records and create a list with the returned data
    query_result = session.query(RealState).all()
    print('')
    print(f"Current records on database: {len(query_result)}.")


# for jj in range(12,14):

scrapy_real_state(23)