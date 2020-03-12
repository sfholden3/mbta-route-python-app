from api import getRouteNames, getRouteAndStops
from data import routeIdList, routesAndStops, oneRouteManyStops, oneStopManyRoutes, createRouteGraph, getAssociatedRoutesPerStop, convertStopToRoutes
from calculations import calculateAndPrintMinMax, routesRequired

# Idea: we can hit this file to get more details information about the MBTA routes
# This information should help determine if I am correctly answering the routing questions

# Get list of stops to request

# get more information about a particular stop

# route graph (key to see if it's returning the correct results)

import sys, getopt

def info(argv):
    showStopInfo = False
    showGraph = False
    try:
        opts, args = getopt.getopt(argv,"sg",["stops=","graph="])
    except getopt.GetoptError:
        print('main.py -s -g')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--stops"):
            showStopInfo = True
        elif opt in ("-g", "--graph"):
            showGraph = True
    if showStopInfo:
        routeIds = routeIdList()
  
        routeList, stopList = routesAndStops(routeIds)       
    
        combined_stops = oneStopManyRoutes(stopList)
        combined_stops.set_index('stop_id', inplace=True)
        stop_dict = combined_stops.to_dict()['uroutes']
        print("Stop Ids: ")
        print(stop_dict.keys())
    if showGraph:
        routeIds = routeIdList()

        routeList, stopList = routesAndStops(routeIds)       
    
        combined_routes = oneRouteManyStops(routeList)
    

        combined_stops = oneStopManyRoutes(stopList)

        hubs = combined_stops[combined_stops['uroutes'].apply(lambda x: len(x) > 1)]
        hubs.set_index('stop_id', inplace=True, drop=True)

        route_graph = createRouteGraph(combined_routes, hubs)
        print(route_graph)
        
                


if __name__ == "__main__":
   info(sys.argv[1:])