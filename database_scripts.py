from sqlalchemy import exc
from address_coordinates import address_coordinates

# def addtodatabase(listings, RealState, db):
#     """
#     To add a list of records to the database
#     """

#     records_added = 0
#     n = 1
#     for item in listings:

#         print('----------------------------------------')
#         print(n)
#         price = int(item["Price"])
#         address = item["Address"]
#         house_link = item["Link"]
#         photolink = item["Photo link"]

#         coordinates = address_coordinates(address)
#         if coordinates['Valid']:
#             latitude = coordinates['Latitude']
#             longitude = coordinates['Longitude']
#             map_link = coordinates['Map_link']
            

#             # Create an instance with the data
#             house = RealState(
#                 price = price,
#                 address = address,
#                 house_link = house_link,
#                 photolink = photolink,
#                 latitude = latitude,
#                 longitude = longitude,
#                 map_link = map_link
#                 )
#         else:
#             # Create an instance with the data
#             house = RealState(
#                 price = price,
#                 address = address,
#                 house_link = house_link,
#                 photolink = photolink
#                 )
    
#         # Add recordes to database
#         try:
#             db.session.add(house)
#             db.session.commit()
#             records_added = records_added + 1
        
#         # To handle the duplicated entry
#         except exc.IntegrityError:
#             db.session.rollback()
#             print('Duplicated Entry')

#         n = n + 1

#     return records_added

def addonetodatabase(item, RealState, db):
    """
    To add one record to the database
    """
    price = int(item["Price"])
    address = item["Address"]
    house_link = item["Link"]
    photolink = item["Photo link"]
    
    coordinates = address_coordinates(address)
    if coordinates['Valid']:
        latitude = coordinates['latitude']
        longitude = coordinates['longitude']
        map_link = coordinates['map_url']
        

        # Create an instance with the data
        house = RealState(
            price = price,
            address = address,
            house_link = house_link,
            photolink = photolink,
            latitude = latitude,
            longitude = longitude,
            map_link = map_link
            )
    else:
        # Create an instance with the data
        house = RealState(
            price = price,
            address = address,
            house_link = house_link,
            photolink = photolink
            )

    # Add recordes to database
    try:
        db.session.add(house)
        db.session.commit()
        result = True
    
    # To handle the duplicated entry
    except exc.IntegrityError:
        db.session.rollback()
        print('Duplicated Entry')
        result = False

    print(f"Record added: {result}")

    return result