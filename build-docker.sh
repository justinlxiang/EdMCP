#!/bin/bash
docker build -t edmcp .
echo "Docker image 'edmcp' built successfully" 
docker tag edmcp justinxiang05/edmcp:latest
docker push justinxiang05/edmcp:latest
echo "Docker image 'edmcp' pushed to Docker Hub successfully"