# PROOF OF CONCEPT borrowed from https://www.youtube.com/watch?v=IG1QioWSXRI&feature=youtu.be
# we're weighting all routes the same 
weight = 1

def getShortestPath(graph,start,goal):
    shortest_distance = {}
    pre = {}
    unseenNodes = graph
    inf = 999999999
    path = []
    for node in unseenNodes:
        shortest_distance[node] = inf
    shortest_distance[start] = 0
    
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                minNode = node
        for childNode in graph[minNode]:
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                pre[childNode] = minNode
        unseenNodes.pop(minNode)
    
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0, currentNode)
            currentNode = pre[currentNode]
        except KeyError:
            print("path not reachable")
            break
    path.insert(0, start)
    if shortest_distance[goal] != inf:
        return path, shortest_distance[goal]
