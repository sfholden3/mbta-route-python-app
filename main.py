import json
import pandas as pd
from api import getRouteNames, getRouteAndStops
from data import routeIdList, routesAndStops, oneRouteManyStops, oneStopManyRoutes
from calculations import calculateAndPrintMinMax

# Perform API request for MBTA Routes of type 0,1
# Print long_name of each route
# Return list of ids for routes to be used in other API requests
routeIds = routeIdList()
  
# Perform API request to gather the relationships between routes and stops
# Shape the data into two formats: 
# 1. One stop, to all related routes
# 2. One route, to all related stops
routeList, stopList = routesAndStops(routeIds)       
    
combined_routes = oneRouteManyStops(routeList)

calculateAndPrintMinMax(combined_routes)

combined_stops = oneStopManyRoutes(stopList)

hubs = combined_stops[combined_stops['uroutes'].apply(lambda x: len(x) > 1)]
print("Stops associated with more than one route:")
print(hubs)
    
    
           
