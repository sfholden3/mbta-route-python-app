
import copy

def calculateAndPrintMinMax(combined_routes):
    max = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.max()]
    min = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.min()]
    print("Max Stops:")
    print(max[['route_id', 'ustops_cnt']])
    print("Min Stops:")
    print(min[['route_id', 'ustops_cnt']])
    print('\n')

# weighting all route switches the same
weight = 1
# large number to outweight any actual path weight
large_num = 1000000000
#Dijkstra Algorithm
# Resources: https://www.youtube.com/watch?v=IG1QioWSXRI&feature=youtu.be
def routesRequired(route_graph, stop_from, stop_to):
    # create copy to track which routes have been visited
    unVisitedRoutes = copy.deepcopy(route_graph)
    # init the graph with weights. All nodes except the starting node are set to equivalent of infinity
    weighted_graph = {}
    for node in route_graph:
        weighted_graph[node] = large_num
    weighted_graph[stop_from] = 0
    shortest_dist = large_num
    previous = {}
    path = []

    # visit all the nodes, removing them from the list once visited
    while unVisitedRoutes:
        minRoute = None
        #check neighboring nodes for shortest path
        #Greedy algorithm: determine the shortest next step and take that step.
        for node in unVisitedRoutes:
            if minRoute is None:
                minRoute = node
            if weighted_graph[node] < weighted_graph[minRoute]:
                minRoute = node
            
        # check all of the directly connected routes
        # set the path of this route according to the shortest path to it
        for related_route in route_graph[minRoute]:
            if (weight + weighted_graph[minRoute]) < weighted_graph[related_route]:
                weighted_graph[related_route] = weight + weighted_graph[minRoute]
                previous[related_route] = minRoute
        unVisitedRoutes.pop(minRoute)

    #iterate back over the steps in order to find the path
    currentRoute = stop_to
    while currentRoute != stop_from:
        try:
            path.insert(0, currentRoute)
            currentRoute = previous[currentRoute]
        except KeyError:
            print("path not reachable")
            break
    path.insert(0, stop_from)
    return path, weighted_graph[stop_to]

            
            
    
    