from math import pi, acos, sin, cos
import heapq

''' Maps a Node ID to a tuple of lat/lng coordinates '''
nodeToCoordinates = {}

''' Maps a Node ID to a set of all neighboring nodes '''
nodeToNeighbors = {}

''' Maps the two path nodes back to their original path ID '''
nodesToPath = {}

def run(source, destination, paths, nodes):
    _init(paths, nodes)
    
    astar_route, astar_checked = astar(source, destination)
    dijkstra_route, dijkstra_checked = dijkstra(source, destination)

    return ((astar_route, astar_checked), (dijkstra_route, dijkstra_checked))

def _init(paths, nodes):
    '''
        Initializes the nodeToCoordinates and nodeToNeighbors dictionaries.
    '''

    for p in paths:
        if not p['source'] in nodeToNeighbors:
            nodeToNeighbors[p['source']] = set()

        nodeToNeighbors[p['source']].add(p['destination'])
        
        if not p['destination'] in nodeToNeighbors:
            nodeToNeighbors[p['destination']] = set()
        
        nodeToNeighbors[p['destination']].add(p['source'])

        nodesToPath[p['source'] + p['destination']] = p['id']
        nodesToPath[p['destination'] + p['source']] = p['id']

    for n in nodes:
        nodeToCoordinates[n['id']] = (n['lat'], n['lng'])

def astar(source, destination):
    '''
        Performs an A* Graph search, returning the set of checked path IDs
        The priority queue contains tuples of the following form (h, f, g, curr, from)
        where:
            f = g + h
            g = distance travelled in this path
            h = heuristic future distance estimate
            path = list of path IDs we are currently evaluating
    '''

    checked_paths = set()
    popped_nodes = set()
    h_initial = distance(source, destination)
    p_initial = (h_initial, 0, h_initial, [source]) 
    pq = [p_initial]                            
                                                
    while pq:                                   
        f, g, h, node_path = heapq.heappop(pq)

        last_node =  node_path[-1]
        
        if len(node_path) > 1:
            checked_paths.add(nodesToPath[last_node + node_path[-2]])

        if last_node == destination:
            return (node_path, checked_paths)

        if last_node not in popped_nodes:
            for neighbor in nodeToNeighbors[last_node]:
                new_g = g + distance(last_node, neighbor)
                new_h = distance(neighbor, destination)
                new_f = new_g + new_h
                new_path = list(node_path)
                new_path.append(neighbor)
                pq_node = (new_f, new_g, new_h, new_path)
                heapq.heappush(pq, pq_node)

        popped_nodes.add(last_node)

def dijkstra(source, destination):
    '''
        Perform's Dijkstra's algorithm to find the shortest path between two nodes
        in the graph. The priority queue here contains tuples of the form (g, path)
        where:
            g = distance travelled thus far
            path = the list of path IDs we are currently evaluating
    '''

    pq = [(0, [source])]
    checked_paths = set()
    popped_nodes = set()

    while pq:
        g, node_path = heapq.heappop(pq)
        last_node = node_path[-1]

        if len(node_path) > 1:
            checked_paths.add(nodesToPath[last_node + node_path[-2]])
        
        if last_node == destination:
            return (node_path, checked_paths)

        if last_node not in popped_nodes:
            for neighbor in nodeToNeighbors[last_node]:
                new_g = g + distance(last_node, neighbor)
                new_path = list(node_path)
                new_path.append(neighbor)

                heapq.heappush(pq, (new_g, new_path))

        popped_nodes.add(last_node)


distances = {}
R = 3958.76 # Radius of Earth, used in great circle distance calculation.
def distance(source, destination):
    '''
        Lazily calculates distance between two nodes and memoizes the result.
        param source - string ID of source node
        param destination - string ID of destination node
    '''

    if source + destination in distances:
        return distances[source + destination]
    
    if destination+source in distances: 
        return distances[destination + source]

    if source == destination:
        return 0

    x1, y1 = nodeToCoordinates[source]
    x2, y2 = nodeToCoordinates[destination]

    x1 *= pi / 180
    y1 *= pi / 180
    x2 *= pi / 180
    y2 *= pi / 180

    d = acos(sin(x1) * sin(x2) + cos(x1) * cos(x2) * cos(y2 - y1)) * R
    distances[source+destination] = d
    return d

