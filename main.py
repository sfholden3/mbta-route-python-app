import json
import pandas as pd
from api import getRouteNames, getRouteAndStops
from data import routeIdList, routesAndStops, oneRouteManyStops, oneStopManyRoutes, createRouteGraph, getAssociatedRoutesPerStop, convertStopToRoutes
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
    
    # Question 2, part 1 & 2
    calculateAndPrintMinMax(combined_routes)

    combined_stops = oneStopManyRoutes(stopList)

    # Question 2, part 3
    hubs = combined_stops[combined_stops['uroutes'].apply(lambda x: len(x) > 1)]
    print("Stops associated with more than one route:")
    hubs.set_index('stop_id', inplace=True, drop=True)
    print(hubs)

    # Question 3
    # create route graph to be used to find shortest path
    route_graph = createRouteGraph(combined_routes, hubs)    

    # Convert stops to associated routes
    start_route, end_route = convertStopToRoutes(combined_stops, startStop, endStop)

    # if the start and end stops both have the same associated route, then we have the reccommended route
    if len(set(start_route).intersection(set(end_route))) > 0:
        intersection_routes = set(start_route).intersection(set(end_route))
        print(' OR '.join(intersection_routes))
        sys.exit()
    if len(start_route) == 1 and len(end_route) == 1:
        path, shortest_distance = routesRequired(route_graph, start_route[0], end_route[0])
        print(path)
        print(shortest_distance)
        sys.exit()
    # if multiple hubs are compared, find the shortest path
    # Improvement: There are more efficient ways to do this rather than running it for each combo
    if len(start_route) > 1 or len(end_route) > 1:
        shortest_path = []
        lowest_cost = 99999999999
        shared_string = ''
        for s_rt in start_route:
            for e_rt in end_route:
                _path, _shortest_distance = routesRequired(route_graph, s_rt, e_rt)
                if _shortest_distance < lowest_cost:
                    lowest_cost = _shortest_distance
                    shortest_path = _path
                    shared_string = ', '.join(_path)
                if _shortest_distance == lowest_cost:
                    this_string = ', '.join(_path)
                    shared_string = shared_string + ' OR ' + this_string
        print(shared_string)
        print(lowest_cost) 
        sys.exit()                


if __name__ == "__main__":
   main(sys.argv[1:])
