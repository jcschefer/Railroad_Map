import searcher
from railroad_server import RailroadServer

from random import choice
from sys import argv, exit

class SearcherTest(RailroadServer):
    '''
        Tests the searcher file by generating random source and destination nodes, verifying that the shortest paths found by both A* and Dijkstra are equal.
    '''
    
    def test(self, n):
        nodes = list(self.nodes.keys())

        for i in range(n):
            source = choice(nodes)
            destination = choice(nodes)

            astar, dijkstra = searcher.run(source, destination, self.paths.values(), self.nodes.values())

            if astar[0] != dijkstra[0]:
                print('Test failed:\n\tsource: ' + source + '\n\tdestination: ' + destination + '\n\tastar: ' + str(astar[0]) + '\n\tdijkstra: ' + str(dijkstra[0]))
                exit(1)
            

if __name__ == '__main__':
    num_trials = 10

    if len(argv) > 1:
        num_trials = int(argv[1])

    tester = SearcherTest()
    #tester._init()

    tester.test(num_trials)
