from api import getRouteAndStops, getRouteNames
import pandas as pd

# Perform API request for MBTA Routes of type 0,1
# Print long_name of each route
# Return list of ids for routes to be used in other API requests
def routeIdList():
    response = getRouteNames()
    
    json_resp = response.json()
    resp_data = json_resp["data"]
    
    route_id_list = []
    route_long_names = []
    print('\n')
    print("MBTA Train Routes:")
    for data in resp_data:
        id = data['id']
        name = data['attributes']['long_name']
        route_id_list.append(id)
        print(name)
    print('\n')
    # return list of route ids to be used in other queries
    return ','.join(map(str, route_id_list))

# Perform API request to gather the relationships between routes and stops
# Shape the data into two formats: 
# 1. One stop, to all related routes
# 2. One route, to all related stops
def routesAndStops(routeIds):
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
    return routeList, stopList


# Returns dataframe with the following 3 columns:
# 1. route_id
# 2. ustops: list of unique stops
# 3. ustops_cnt: count of the unique stops
def oneRouteManyStops(routeList):
    route_df = pd.DataFrame(routeList)
    # We may want to remove "shuttles"
    route_df = route_df[~route_df['route_id'].str.contains('Shuttle')]
    # Get stops associated with route into one entry
    combined_routes = route_df.groupby('route_id').agg({'stops': 'sum'}).reset_index()
    # Get down to only the unique stops per route
    combined_routes['ustops'] = combined_routes['stops'].apply(lambda x: list(set(x)))
    # unqiue route count
    combined_routes['ustops_cnt'] = combined_routes['ustops'].apply(lambda x: len(x))
    
    return combined_routes

# Returns dataframe with the following 3 columns:
# 1. stop_id
# 2. uroutes: list of unique stops
def oneStopManyRoutes(stopList):
    stop_df = pd.DataFrame(stopList)
    # We may want to remove "shuttles"
    stop_df = stop_df[~stop_df['route_id'].str.contains('Shuttle')]
    # Get stops associated with route into one entry
    combined_stops = stop_df.groupby('stop_id').agg({'route_id': lambda x: ', '.join(x)}).reset_index()
    combined_stops['routes'] = combined_stops['route_id'].apply(lambda x: x.split(', '))
    combined_stops['uroutes'] = combined_stops['routes'].apply(lambda x: list(set(x)))
    return combined_stops[['stop_id', 'uroutes']]
    