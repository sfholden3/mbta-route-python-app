import requests

api_url_base = 'https://api-v3.mbta.com/'
headers = {'Content-Type': 'application/json'}

routes_arg = 'routes?filter[type]=0,1'
def getRouteNames():
    resp = requests.get(api_url_base+routes_arg, headers=headers)
    if resp.status_code == 200:
        return resp
    print('Error: getRouteNames API endpoint')

    
shape_arg = '/shapes?filter[route]='
include_arg = '&include=stops'
def getRouteAndStops(routes):
    api_url = api_url_base+shape_arg+routes+include_arg
    print(api_url)
    resp = requests.get(api_url, headers=headers)
    if resp.status_code == 200:
        return resp
    print('Error: getRouteNames API endpoint')

