import requests


def get_coordinates(address):
    """ 
    Retrieve the coordinates of a given address using Nominatim
    """
    # https://nominatim.org/
    url_address = 'https://nominatim.openstreetmap.org/search?q='
    searchformat = '&format=json&polygon_geojson=1&addressdetails=1'
    
    # Format address to search for coordinates
    address_string = address.split(' ')
    x = "+".join(address_string)
    address_search = x.replace(',','')
    coordinate_search = f"{url_address}{address_search}{searchformat}"
    
    #  Perform a request for data
    response_coordinates = requests.get(coordinate_search).json()
    
    # return the rounded coordinates if exists
    if response_coordinates:
        lat = round(float(response_coordinates[0]['lat'])*100)/100
        lon = round(float(response_coordinates[0]['lon'])*100)/100
        
        return {"latitude": lat, "longitude": lon}


# get_coordinates('13414 Boca Raton Dr, Houston, TX 77069')