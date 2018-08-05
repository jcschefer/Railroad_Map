import grpc

from . import messages_pb2
from . import messages_pb2_grpc

PORT = 'localhost:50051'

def get_all_paths():
    with grpc.insecure_channel(PORT) as channel:
        stub = messages_pb2_grpc.RailroadBackendStub(channel)
        response = stub.GetAllPaths(messages_pb2.Empty())

    return response

def perform_search(source, destination):
    with grpc.insecure_channel(PORT) as channel:
        stub = messages_pb2_grpc.RailroadBackendStub(channel)
        response = stub.PerformSearch(messages_pb2.PerformSearchRequest(
            source=source,
            destination=destination))
    
    return response
