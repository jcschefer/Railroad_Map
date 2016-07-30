# Jack Schefer, 2/3/16
#
from time import time
from math import pi,acos,sin,cos
from sys  import argv
import heapq
#
#
START = 'Washington DC'
if len(argv) > 1: START = argv[1]
END   = 'Minneapolis'
if len(argv) > 2: END = argv[2]
#
tempList = open('rrNodes.txt').read().split()
neighborlist = open('rrEdges.txt').read().split()
#
nameSwapper = {}
#
lines = list(open('rrNodeCity.txt'))
stripped = []
for l in lines:
  stripped.append(l.rstrip())
lines = stripped
for l in lines:
  code = l[:7]
  name = l[8:]
  nameSwapper[ code ] = name
  nameSwapper[ name ] = code
#
#
nodeToCoordinates = {}  # maps the letter to a tuple of the x and y coordinates
nodeToNeighbors = {}    # maps the letter to a list of neighbors
nodesToDistance = {}    # maps a tuple of nodes to the distance, both directions ok
#
i = 0
#
while i < len(tempList):
  code = tempList[i]
  y = float(tempList[i + 1])
  x = float(tempList[i + 2])
  i += 3
  nodeToCoordinates[code] = (x,y)
  if code in nameSwapper: nodeToCoordinates[ nameSwapper[code] ] = (x,y)
  #
#
i = 0
while i < len(neighborlist)-1:
  first = str(neighborlist[i])
  second = str(neighborlist[i+1])
  i += 2
  #
  if first in nodeToNeighbors: nodeToNeighbors[first].append(second)
  else: nodeToNeighbors[first] = [second]
  if second in nodeToNeighbors: nodeToNeighbors[second].append(first)
  else: nodeToNeighbors[second] = [first]
  #
#
#
#
#
def distance(node1, node2):
  if (node1,node2) in nodesToDistance: return nodesToDistance[ (node1,node2) ]
  if node1==node2: return 0
  x1, y1 = nodeToCoordinates[node1]
  x2, y2 = nodeToCoordinates[node2]
  #d = math.sqrt((x2-x1)**2 + (y2-y1)**2)
  R = 3958.76
  x1 *= pi/180
  x2 *= pi/180
  y1 *= pi/180
  y2 *= pi/180
  d = acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) )* R
  nodesToDistance[ (node1,node2) ] = d
  nodesToDistance[ (node2,node1) ] = d
  return d
#
########################################################################
#
def astar(nodeToNeighbors, first, target): #returns a tuple containing the path, followed by the distance traveled, followed by the size of the cf closed set
  #
  pq = []                      #contents: (f, g, h, list) 
  h = distance(first, target)
  checkedPaths = set()
  qSet = 0
  p = (h, 0, h, [first])
  pq.append(p)
  heapq.heapify(pq)
  check = []
  while pq:
    #
    t = heapq.heappop(pq)
    tF, tG, tH, tPath = t
    lastNode = tPath[len(tPath) - 1]
    if len(tPath) > 1: checkedPaths.add( (lastNode, tPath[len(tPath)-2]) )
    #
    if lastNode == target or lastNode is target: return (tPath,tG,qSet+1, checkedPaths)
    #
    if lastNode not in check:
      qSet += 1
      for neighbor in list(nodeToNeighbors[lastNode]):
        nG = tG + distance(lastNode,neighbor)
        nH = distance(neighbor, target)
        nF = nG + nH
        nPath = list(tPath)
        nPath.append(neighbor)
        t = (nF, nG, nH, nPath)
        heapq.heappush(pq,t)
    #
    check.append(lastNode)
  #
#
########################################################################
#
def isCode(s):
  if len(s) != 7: return False
  if s[0]=='0' or s[0]=='1' or s[0]=='2' or s[0]=='3' or s[0]=='4' or s[0]=='5' or s[0]=='6' or s[0]=='7' or s[0]=='8' or s[0]=='9': return True
  return False
#
########################################################################
#
def dijkstra(nodeToNeighbors, first, target):
  pq = []    #to contain (g, list)
  qSet = 0
  check = []
  checkedPaths = set()
  if not isCode(first): first = nameSwapper[first]
  if not isCode(target): target = nameSwapper[target]
  heapq.heappush(pq, (0,[first]) )
  while pq:
    tG,tPath = heapq.heappop(pq)
    lastNode = tPath[len(tPath)-1]
    #
    if lastNode == target or lastNode is target: return (tPath, tG, qSet+1, checkedPaths)
    if len(tPath) > 1: checkedPaths.add( (lastNode, tPath[len(tPath)-2]) )
    if lastNode not in check:
      qSet += 1
      for n in list(nodeToNeighbors[lastNode]):
        nPath = list(tPath)
        nPath.append(n)
        nG = tG + distance(lastNode, n)
        t = (nG,nPath)
        heapq.heappush(pq,t)
    check.append(lastNode)
#
########################################################################
#
if __name__ == '__main__':
  #
  START = nameSwapper[START]
  END   = nameSwapper[END]
  #
  astar_long = []
  astar_lat  = [] 
  bfs_long   = [] 
  bfs_lat    = [] 
  other_long = [] 
  other_lat  = [] 
  #
  print('starting Astar search...')
  aPath,g1,closedSet,astarChecked = astar(nodeToNeighbors, START, END)
  print('Astar search finished...')
  print('starting Dijkstra search...')
  dPath,g2,closeset,dijkstraChecked = dijkstra(nodeToNeighbors, START, END)
  print('Dijkstra search finished...')
  #
  astarChecked    = set(astarChecked)
  dijkstraChecked = set(dijkstraChecked)
  #
  allPaths = set()
  i = 0
  while i < len(neighborlist):
    allPaths.add( (neighborlist[i], neighborlist[i + 1]) )
    i += 2
    #
  #
  for p in allPaths:
    start,end = p
    o = (end,start)
    longout = None
    latout  = None
    #
    numOther = 0
    #
    if p in astarChecked or o in astarChecked: 
      longout = astar_long
      latout  = astar_lat
    #
    elif p in dijkstraChecked or o in dijkstraChecked:
      longout = bfs_long
      latout  = bfs_lat
    #
    else: 
      numOther += 1
      longout = other_long
      latout  = other_lat
    #
    long1, lat1 = nodeToCoordinates[start]
    long2, lat2 = nodeToCoordinates[end]
    longout.append(str(long1))
    longout.append(str(long2))
    latout.append( str(lat1 ))
    latout.append( str(lat2 ))
    #
  #
  ##########################################################################
  #
  # Make the js resource file
  filename = 'js_resources.js'
  out = open(filename , 'w')
  #
  # Astar printing
  out.write('var gastarLat = function(){ return [')
  for i in range(len(astar_lat)):
    #
    joiner = ''
    if i != len(astar_lat) - 1: joiner += ', '
    #
    out.write(astar_lat[i] + joiner)
    #
  #
  out.write('];}\n')
  #
  out.write('var gastarLong = function(){ return [')
  for i in range(len(astar_long)):
    #
    joiner = ''
    if i != len(astar_long) - 1: joiner += ', '
    #
    out.write(astar_long[i] + joiner)
    #
  #
  out.write('];}\n')
  #
  # BFS printing
  out.write('var gdijkstraLat = function(){ return [')
  for i in range(len(bfs_lat)):
    #
    joiner = ''
    if i != len(bfs_lat) - 1: joiner += ', '
    #
    out.write(bfs_lat[i] + joiner)
    #
  #
  out.write('];}\n')
  #
  out.write('var gdijkstraLong = function(){ return [')
  for i in range(len(bfs_long)):
    #
    joiner = ''
    if i != len(bfs_long) - 1: joiner += ', '
    #
    out.write(bfs_long[i] + joiner)
    #
  #
  out.write('];}\n')
  #
  # Remaining printing
  out.write('var gotherLat = function(){ return [')
  for i in range(len(other_lat)):
    #
    joiner = ''
    if i != len(other_lat) - 1: joiner += ', '
    #
    out.write(other_lat[i] + joiner)
    #
  #
  out.write('];}\n')
  #
  out.write('var gotherLong = function(){ return [')
  for i in range(len(other_long)):
    #
    joiner = ''
    if i != len(other_long) - 1: joiner += ', '
    #
    out.write(other_long[i] + joiner)
    #
  #
  out.write('];}\n')
  #
  out.write('console.log(\'Data loaded succesfully!\')')
  out.close()
  #
#
#
# End of file.
