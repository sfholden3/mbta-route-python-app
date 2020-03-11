import requests

api_url_base = 'https://api-v3.mbta.com/'
headers = {'Content-Type': 'application/json'}

routes_arg = 'routes?filter[type]=0,1'
def getRouteNames():
    return requests.get(api_url_base+routes_arg, headers=headers)
    
shape_arg = '/shapes?filter[route]='
include_arg = '&include=stops'
def getRouteAndStops(routes):
    api_url = api_url_base+shape_arg+routes+include_arg
    print(api_url)
    return requests.get(api_url, headers=headers)