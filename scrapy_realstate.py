import os
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time


def scraped_data(page_number):
    # identify location of chromedriver and store it as a variable
    driverPath = ["/usr/local/bin/chromedriver"]  # For MacBook

    # Setup configuration variables to enable Splinter to interact with browser
    executable_path = {'executable_path': driverPath[0]}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url_realtor = "https://www.realtor.com/realestateandhomes-search/Houston_TX/type-single-family-home/price-"
    link_details = "https://www.realtor.com"
    min_price = '250000'
    max_price = '300000'
    sort_by = '/sby-2' # Highest to lowest price

    query_url = f"{url_realtor}{min_price}-{max_price}{sort_by}/pg-{page_number}"
    # print(query_url)

    # Use the browser to visit the url
    browser.visit(query_url)

    # Wait for 5 seconds for error purpouses
    time.sleep(20)

    # Return the rendered page by the browser
    html_realtor = browser.html

    # Use beatifulsoup to scrap the page rendered by the browser
    soup = BeautifulSoup(html_realtor, 'html.parser')

    # Search for the div where the title is located
    results = soup.find_all('div', class_="card-box")
    
    # Print results and save to a dictionary
    n = 1
    realstate_list = []
    for result in results:
    #     Clear the variables to not store repeated info
        house_price = ''
        address = ''
        link_page = ''
                    
        n = n + 1
        if not result.find('div', class_="ads"):
    #         print(f'Result: {n} of {len(results)}')
            price_div = result.find('div', class_="price")
            house_price = price_div.find('span').text.split('$')[-1]
            link_page = result.find('a')['href']
            img_label = result.find('img')
            address = img_label['alt']
# 
            
            # Save results to a dictionary
            realstate_list.append(
                {
                    "Price": int(house_price.replace(',','')),
                    "Address": address,
                    "Link": str(link_details+link_page)
                }
            )
    
        else:
            print('Data not available or Advertise.')
    
    # When you’ve finished testing, close your browser using browser.quit:
    browser.quit()

    print(f"Items on the web page: {len(realstate_list)}.")
        
    return realstate_list
