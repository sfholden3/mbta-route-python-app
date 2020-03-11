import json
import pandas as pd
from api import getRouteNames, getRouteAndStops
from routeInfo import routeIdList

routeIds = routeIdList()  
# create dictionary with route and stop information
routeList = []
stopList = []
stop_resp = getRouteAndStops(routeIds)
stop_route_json = stop_resp.json()["data"]
for stop_route in stop_route_json:
    route_id = stop_route['relationships']['route']['data']['id']
    stop_lst = stop_route['relationships']['stops']['data']
    stops = []
    for stop in stop_lst:
        stops.append(stop['id'])
        stopList.append({
            "stop_id": stop['id'],
            "route_id": route_id
        })
    routeList.append({
        "route_id": route_id,
        "stops": stops
    })
        
    
route_df = pd.DataFrame(routeList)
# We may want to remove "shuttles"
route_df = route_df[~route_df['route_id'].str.contains('Shuttle')]
# Get stops associated with route into one entry
combined_routes = route_df.groupby('route_id').agg({'stops': 'sum'}).reset_index()
#count all stops
combined_routes['stops_cnt'] = combined_routes['stops'].apply(lambda x: len(x))
# Get down to only the unique stops per route
combined_routes['ustops'] = combined_routes['stops'].apply(lambda x: list(set(x)))
# unqiue route count
combined_routes['ustops_cnt'] = combined_routes['ustops'].apply(lambda x: len(x))
print(combined_routes.describe())
max = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.max()]
min = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.min()]
print(max)
print(min)
    
stop_df = pd.DataFrame(stopList)
# We may want to remove "shuttles"
stop_df = stop_df[~stop_df['route_id'].str.contains('Shuttle')]
# Get stops associated with route into one entry
combined_stops = stop_df.groupby('stop_id').agg({'route_id': lambda x: ', '.join(x)}).reset_index()
combined_stops['routes'] = combined_stops['route_id'].apply(lambda x: x.split(', '))
combined_stops['uroutes'] = combined_stops['routes'].apply(lambda x: list(set(x)))
hubs = combined_stops[combined_stops['uroutes'].apply(lambda x: len(x) > 1)]
print(hubs)
    
    
           
