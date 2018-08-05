import messages_pb2_grpc
import messages_pb2
from concurrent import futures
import grpc

import json
import time
import os
import os.path

import searcher

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_PORT = 'localhost:50051'

NODES_FNAME = os.path.join(os.path.dirname(__file__), 'data', 'nodes.json')
PATHS_FNAME = os.path.join(os.path.dirname(__file__), 'data', 'paths.json')

class RailroadServer(messages_pb2_grpc.RailroadBackendServicer):
    '''
        Private members:
            - nodes: a dictionary mapping node IDs to the node itself (id, lat, lng)
            - paths: a dictionary mapping path IDs to the path itself (id, source ID, destination ID)

        TODO: store this in a DB rather than JSON loaded into dictionaries...
    '''

    def __init__(self):
        with open(NODES_FNAME, 'r') as f:
            nodelist = json.load(f)
            self.nodes = dict((n['id'], n) for n in nodelist)
        with open(PATHS_FNAME, 'r') as f:
            pathlist = json.load(f)
            self.paths = dict((p['id'], p) for p in pathlist)

    def _buildNodeProtoFromId(self, node_id):
        return messages_pb2.Node(
            key=node_id,
            lat=self.nodes[node_id]['lat'],
            lng=self.nodes[node_id]['lng'])

    def _buildPathProtoFromId(self, path_id):
        return messages_pb2.Path(
            key=path_id,
            source=self._buildNodeProtoFromId(self.paths[path_id]['source']),
            destination=self._buildNodeProtoFromId(self.paths[path_id]['destination']))
    
    def GetAllPaths(self, request, context):
        return messages_pb2.GetAllPathsResponse(
            path=[self._buildPathProtoFromId(path_id) for path_id in self.paths.keys()]
        )

    def PerformSearch(self, request, context):
        astar, dijkstra = searcher.run(request.source,  request.destination, self.paths.values(), self.nodes.values())

        assert astar[0] == dijkstra[0]
        return messages_pb2.PerformSearchResponse(
            a_star_keys=list(astar[1]),
            dijkstra_keys=list(dijkstra[1])
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))

    backend_instance = RailroadServer()
    #backend_instance._init()
    
    messages_pb2_grpc.add_RailroadBackendServicer_to_server(backend_instance, server)
    server.add_insecure_port(_PORT)
    server.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
