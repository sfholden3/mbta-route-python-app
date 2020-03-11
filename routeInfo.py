from api import getRouteNames

# Perform API request for MBTA Routes of type 0,1
# Print long_name of each route
# Return list of ids for routes to be used in other API requests
def routeIdList():
    response = getRouteNames()
    
    json_resp = response.json()
    resp_data = json_resp["data"]
    
    route_id_list = []
    route_long_names = []
    for data in resp_data:
        id = data['id']
        name = data['attributes']['long_name']
        route_id_list.append(id)
        print(name)
        
    # return list of route ids to be used in other queries
    return ','.join(map(str, route_id_list))
    
    