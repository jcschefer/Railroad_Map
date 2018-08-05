#!/bin/bash

# Builds the protos and boilerplate gRPC code, starts server
cd service
./build_protos.sh

python3 railroad_server.sh
