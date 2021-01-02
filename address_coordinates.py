import requests
import os

try:
    from api_keys import positionstack_key, opencagedata_API
except ModuleNotFoundError:
    positionstack_key = os.environ['positionstack_key']

def nominatim_coordinates(address):    
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
    
    # Handle empty results
    if not response_coordinates:
        valid_result = False
        print("No result found")
        return {"Valid": valid_result}
        
    else:
        valid_result = True
        print(response_coordinates)
    
        # return coordinates
        latitude = float(response_coordinates[0]['lat'])
        longitude = float(response_coordinates[0]['lon'])

        map_url = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}"
        print(f"Map: {map_url}")

        return {"Valid": valid_result,"latitude": latitude, "longitude": longitude, "map_url": map_url}

def positiontrack_coordinates(address):
    # Forward Geocoding API Endpoint
    url_positiontrack = f"http://api.positionstack.com/v1/forward?access_key={positionstack_key}&query="
    
    address_lookup = address.replace(" ", "%20")
    url_coordinates = f"{url_positiontrack}{address_lookup}&limit=1"

    print(f"Query URL:")
    print(url_coordinates)
    print('')

    #  Perform a request for data
    response_coordinates = requests.get(url_coordinates).json()
    
    
    # Handle empty results
    if len(response_coordinates['data']) == 0 or len(response_coordinates['data'][0]) == 0:
        valid_result = False
        print("No result found")
        return {"Valid": valid_result}
        
    else:
        valid_result = True
        print(response_coordinates)
    
        # return coordinates
        latitude = response_coordinates['data'][0]['latitude']
        longitude = response_coordinates['data'][0]['longitude']
        
        map_url = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}#map=15/{latitude}/{longitude}"
        print(f"Map: {map_url}")

        return {"Valid": valid_result,"latitude": latitude, "longitude": longitude, "map_url": map_url}




def opencagedata_coordinates(address):
    print('----------------------------------------')
    # Forward Geocoding API Endpoint
    url_opencagedata = 'https://api.opencagedata.com/geocode/v1/json?q='
    api_KEY = f"&key={opencagedata_API}"

    # Houston City Hall Coordinates
    HoustonCityHallCoordinates = "29.760376354375307,-95.3702170895345"
    proximity=f"{HoustonCityHallCoordinates}"
    # Bounds for Houston (https://opencagedata.com/bounds-finder)
    bounds='-95.91830,29.35389,-94.80848,30.26282'  
    
    # Format address to look up
    print(f"Address: {address}")
    address_lookup = address.replace(" ", "%20")
    # Format URL to query
    url_coordinates = f"{url_opencagedata}{address_lookup}{api_KEY}&bounds={bounds}&proximity={proximity}"

    
    #  Perform a request for data
    response_coordinates = requests.get(url_coordinates).json()
    
    
    # Handle empty results
    if len(response_coordinates['results']) == 0:
        valid_result = False
        print("No result found")
        return {"Valid": valid_result}
        
    else:
        valid_result = True
        print(response_coordinates)
    
        # return coordinates
        latitude = response_coordinates['results'][0]['geometry']['lat']
        longitude = response_coordinates['results'][0]['geometry']['lng']
        
        map_url = f"{response_coordinates['results'][0]['annotations']['OSM']['url']}"
        print(f"Map: {map_url}")

        return {"Valid": valid_result,"latitude": latitude, "longitude": longitude, "map_url": map_url}


def address_coordinates(address):
    # Try retrieve coordinates with nominatin

    # Attempt to use only opencagedata
    result_nominatin = opencagedata_coordinates(address)

    # result_nominatin = nominatim_coordinates(address)
    
    # if result not valid use position track
    if not result_nominatin["Valid"]:
        print('Use position track')
        result_positiontrack = positiontrack_coordinates(address)
        # If neither one bring the valid result
        if not result_positiontrack["Valid"]:
            valid_result = False
            print("No result found")
            return {"Valid": valid_result}
        else:
            valid_result = True
            result = result_positiontrack
            latitude = result['latitude']
            longitude = result['longitude']
            map_url = result['map_url']
            return {"Valid": valid_result,"latitude": latitude, "longitude": longitude, "map_url": map_url}
    else:
        valid_result = True
        result = result_nominatin
        latitude = result['latitude']
        longitude = result['longitude']
        map_url = result['map_url']
        return {"Valid": valid_result,"latitude": latitude, "longitude": longitude, "map_url": map_url}