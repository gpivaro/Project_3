import requests
from api_keys import Geo_IPIFY_API

# get client ip address and return ip location
def get_client_ip(request):
    ip_address = request.remote_addr
    if ip_address:
        ip_url = f"https://geo.ipify.org/api/v1?apiKey={Geo_IPIFY_API}&ipAddress={ip_address}"
        #  Perform a request for data
        response = requests.get(ip_url).json()

        return response

