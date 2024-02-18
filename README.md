# Project_3


# Find Your Dream Home Using Machine Learning

* Author: Gabriel Pivaro
* Group name: "Free Solo"

## Summary

Build a web application that stores and displays info about real estate listed to sell in the Houston area. The houses are available for user classification based on the image of the house and features such as price, number of bedrooms, number of bathrooms, square foot, and lot size. The user is presented with three options to classify the real estate: love, like, and dislike. Based on the user classification, the application will suggest houses using Machine Learning algorithms. The application also provides a map for visualization of all the real estate on the database distributed by Zip Codes. 

* Data Source: 
    * Actual data of real estate for sale in the Houston, TX area.
    * Optional: flood risk
    * Google Maps / [opencagedata](https://opencagedata.com/api) coordinates 
    * [GeoJson data of Houston Zip Codes](https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/tx_texas_zip_codes_geo.min.json)
    * [Houston Zip Codes list](https://www.zip-codes.com/city/tx-houston.asp)
    * User classification

* Technologies involved:
    * Python Flask server
    * Postgres SQL database hosted in AWS
    * HTML, CSS, Bootstrap, and JavaScript for data visualization and user interactivity
    * Machine Learning algorithms to study the data and provide suggestions to the user
    * Interactive visualization using JavaScript, D3, Plotly, and Leaflet
    * Heroku for deployment

* Machine Learning:
    * Regression model for the analysis of Price vs. House features (very likely won't perform well)
    * Non-linear model for the analysis of Price vs. House features
    * Image classification to differentiate between 'ugly' and 'beautiful' houses

* Visualization and interactivity:
    * Users can select houses based on their preferences
    * User can select prince range and zip code
    * User can interact with the list of houses selected and get a summary stats of it
    * User can evaluate the houses suggested by the ML to verify the model efficiency
    * Map visualization with houses and zip codes
    * Analytics allow several stats of the real estate and the user preferences



* Deployment:
    * Application video demo [here](https://www.youtube.com/watch?v=6rXyssRe8W8).




---
