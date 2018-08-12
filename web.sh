#!/bin/bash

# Builds the protos and boilerplate gRPC code, starts web server

if [ ! -f service/messages_pb2.py ] || [ ! -f service/messages_pb2_grpc.py ]; then
	cd service
	./build_protos.sh
	cd ..
fi

gunicorn server:app
