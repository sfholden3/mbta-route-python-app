import json
import pandas as pd
from api import getRouteNames, getRouteAndStops


response = getRouteNames()

class Route:
    def __init__(self, id, long_name = ''):
        self.long_name = long_name
        self.id = id
        self.stops = []
        
    def q1(self):
        print(self.long_name)
    
    def addStop(self, newStop):
        self.stops.append(newStop)

class Stop:
    def __init__(self, id):
        self.id = id
        self.routes = []
    
    def addRoute(self, newRoute):
        self.routes.append(newRoute)
    


if response.status_code == 200:
    print('Success!')
    json_resp = response.json()
    tests = json_resp["data"]
    route_id_list = []
    rts = []
    for test in tests:
        id = test['id']
        name = test['attributes']['long_name']
        route_id_list.append(id)
        rts.append(Route(id, name))
    df_routes = pd.DataFrame(rts)
    for rt in rts:
        rt.q1()
    str1 = ','.join(map(str, route_id_list))
    
    # create dictionary with route and stop information
    routeList = []
    stop_resp = getRouteAndStops(str1)
    stop_route_json = stop_resp.json()["data"]
    for stop_route in stop_route_json:
        route_id = stop_route['relationships']['route']['data']['id']
        stop_lst = stop_route['relationships']['stops']['data']
        stops = []
        for stop in stop_lst:
            stop_obj = stops.append(stop['id'])
        newRoute = {
            "route_id": route_id,
            "stops": stops
        }
        routeList.append(newRoute)
        
    
    route_df = pd.DataFrame(routeList)

    # Get stops associated with route into one entry
    combined_routes = route_df.groupby('route_id').agg({'stops': 'sum'})
    #count all stops
    combined_routes['stops_cnt'] = combined_routes['stops'].apply(lambda x: len(x))
    # Get down to only the unique stops per route
    combined_routes['ustops'] = combined_routes['stops'].apply(lambda x: list(set(x)))
    # unqiue route count
    combined_routes['ustops_cnt'] = combined_routes['ustops'].apply(lambda x: len(x))
    print(combined_routes.describe())
    max = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.max()])
    min = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.min()])
    
            
            
    
elif response.status_code == 404:
    print('Not Found.')
