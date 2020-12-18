import requests

url = 'https://ap.rdcpix.com/4c4490b89fdb1f8064f91b214c74f4bfl-m2566284756od-w1024_h768.jpg'
#url = 'http://google.com/favicon.ico'
filename = url.split('/')[-1]
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)
