import requests
from api_keys import positionstack_key

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
    if len(response_coordinates['data'][0]) == 0:
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

def address_coordinates(address):
    # Try retrieve coordinates with nominatin
    result_nominatin = nominatim_coordinates(address)
    
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