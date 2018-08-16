import grpc
import os

from . import messages_pb2
from . import messages_pb2_grpc

PORT = 'localhost:50051'

avoid_grpc = bool(os.getenv('IS_HEROKU', ''))

def get_all_paths():
	if avoid_grpc:
		from . import railroad_server
		stub = railroad_server.RailroadServer()
		return stub.GetAllPaths(messages_pb2.Empty(), None)
	else:
		with grpc.insecure_channel(PORT) as channel:
			stub = messages_pb2_grpc.RailroadBackendStub(channel)
			response = stub.GetAllPaths(messages_pb2.Empty())

			return response

def perform_search(source, destination):
	request = messages_pb2.PerformSearchRequest(
		source=source,
		destination=destination)

	if avoid_grpc:
		from . import railroad_server
		stub = railroad_server.RailroadServer()
		return stub.PerformSearch(request)
	else:
		with grpc.insecure_channel(PORT) as channel:
			stub = messages_pb2_grpc.RailroadBackendStub(channel)
			response = stub.PerformSearch(request)

		return response
