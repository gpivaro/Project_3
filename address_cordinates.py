import requests
from api_keys import positionstack_key

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
        lat = response_coordinates[0]['lat']
        lon = response_coordinates[0]['lon']
        
        map_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}"

        return {"latitude": lat, "longitude": lon, "map_link": map_link}


# get_coordinates('13414 Boca Raton Dr, Houston, TX 77069')

def positiontrack_coordinates(address):
    # Forward Geocoding API Endpoint
    url_positiontrack = f"http://api.positionstack.com/v1/forward?access_key={positionstack_key}&query="
    
    address_lookup = address.replace(" ", "%20")
    url_coordinates = f"{url_positiontrack}{address_lookup}"

    # print(f"Query URL:")
    # print(url_coordinates)
    # print('')

    #  Perform a request for data
    response_coordinates = requests.get(url_coordinates).json()
    # print(f"Results:")
    # print(response_coordinates)
    # print('')

    lat = response_coordinates['data'][0]['latitude']
    lon = response_coordinates['data'][0]['longitude']

    # print(f"Latitude: {lat}")
    # print(f"Longitude: {lon}")

    map_link = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=15/{lat}/{lon}"
    
    return {"latitude": lat, "longitude": lon, "map_link": map_link}
    
# address = "13414 Boca Raton Dr, Houston, TX 77069"
# positiontrack_coordinates(address)