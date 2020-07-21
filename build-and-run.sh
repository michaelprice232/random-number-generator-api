#!/usr/bin/env bash

docker build -t mikeapp .
docker run -p 5000:5000 -d mikeapp:latest