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
#'''
while i < len(tempList):
  code = tempList[i]
  y = float(tempList[i + 1])
  x = float(tempList[i + 2])
  i += 3
  nodeToCoordinates[code] = (x,y)
  if code in nameSwapper: nodeToCoordinates[ nameSwapper[code] ] = (x,y)
  #
#'''
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
  #if not isCode(first): first = nameSwapper[first]
  #if not isCode(target): target = nameSwapper[target]
  pq = []                      #contents: (f, g, h, list) 
  h = distance(first, target)
  checkedPaths = set()
  qSet = 0
  p = (h, 0, h, [first])
  pq.append(p)
  heapq.heapify(pq)
  check = []
  #if not isCode(first): first = nameSwapper[first]
  #if not isCode(target): target = nameSwapper[target]
  while pq:
    #
    t = heapq.heappop(pq)
    tF, tG, tH, tPath = t
    #qSet += 1
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
        #checkedPaths.add( (lastNode, neighbor) )
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
#
#
#
#
def dijkstra(nodeToNeighbors, first, target):
  #numVisited = 0
  pq = []    #to contain (g, list)
  qSet = 0
  #heapq.heappush(pq, (0,[first])  )
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
        #checkedPaths.add( (lastNode, n) )
    check.append(lastNode)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
if __name__ == '__main__':
  #
  START = nameSwapper[START]
  END   = nameSwapper[END]
  #
  astar_long = open('railroadAstarLong.txt'    , 'w')
  astar_lat  = open('railroadAstarLat.txt'     , 'w')
  bfs_long   = open('railroadDijkstraLong.txt' , 'w')
  bfs_lat    = open('railroadDijkstraLat.txt'  , 'w')
  other_long = open('railroadRemainingLong.txt', 'w')
  other_lat  = open('railroadRemainingLat.txt' , 'w')
  #
  aPath,g1,closedSet,astarChecked = astar(nodeToNeighbors, START, END)
  dPath,g2,closeset,dijkstraChecked = dijkstra(nodeToNeighbors, START, END)
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
    longout.write(str(long1) + '\n' + str(long2) + '\n')
    latout.write( str(lat1 ) + '\n' + str(lat2)  + '\n')
    #
  #
  print(len(astarChecked))
  print(len(dijkstraChecked))
  print(numOther)
  print(len(allPaths))
  #
  astar_long.close()
  astar_lat .close()
  bfs_long  .close()
  bfs_lat   .close()
  other_long.close()
  other_lat .close()
  #
#
#
# End of file.
