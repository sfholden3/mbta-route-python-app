import json
import pandas as pd
from api import getRouteNames, getRouteAndStops
from data import routeIdList, routesAndStops, oneRouteManyStops, oneStopManyRoutes, createRouteGraph, getAssociatedRoutesPerStop
from calculations import calculateAndPrintMinMax, routesRequired
import sys, getopt

# Accepting arguments for stops to determine routes
# Resources: https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    startStop = ''
    endStop = ''
    try:
        opts, args = getopt.getopt(argv,"s:e:",["startStop=","endStop="])
    except getopt.GetoptError:
        print('main.py -s <startStop> -e <endStop>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-s", "--startStop"):
            startStop = arg
        elif opt in ("-e", "--endStop"):
            endStop = arg
    print('start stop is '+startStop)
    print('end stop is '+endStop)
   
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
    hubs.set_index('stop_id', inplace=True, drop=True)
    print(hubs)

    # create route graph to be used to find shortest path
    route_graph = createRouteGraph(combined_routes, hubs)    

    # Convert stops to associated routes
    print('\n')
    print("ROUTE:")
    combined_stops.set_index('stop_id', inplace=True)
    stop_dict = combined_stops.to_dict()['uroutes']
    print(stop_dict.keys())
    start_route = getAssociatedRoutesPerStop(startStop, stop_dict)
    end_route = getAssociatedRoutesPerStop(endStop, stop_dict)
    print("Routes associated with starting stop "+startStop+":")
    print(start_route)
    print("Routes associated with ending stop "+endStop+":")
    print(end_route)
    
    print("Routes to take between "+startStop+" and "+endStop+":")
    if len(start_route) < 1 or len(end_route) < 1:
        print("ERROR: invalid stop")
        sys.exit(2)
    # if the start and end stops both have the same associated route, then we have the reccommended route
    if len(set(start_route).intersection(set(end_route))) > 0:
        intersection_routes = set(start_route).intersection(set(end_route))
        print(' OR '.join(intersection_routes))
        sys.exit(2)
    if len(start_route) == 1 and len(end_route) == 1:
        path, shortest_distance = routesRequired(route_graph, start_route[0], end_route[0])
        print(path)
        print(shortest_distance)


if __name__ == "__main__":
   main(sys.argv[1:])
