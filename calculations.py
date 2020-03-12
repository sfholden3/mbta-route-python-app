
def calculateAndPrintMinMax(combined_routes):
    max = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.max()]
    min = combined_routes[combined_routes.ustops_cnt == combined_routes.ustops_cnt.min()]
    print("Max Stops:")
    print(max[['route_id', 'ustops_cnt']])
    print("Min Stops:")
    print(min[['route_id', 'ustops_cnt']])
    print('\n')


#def linesRequired(stop_from, stop_to, combined_stops):
    