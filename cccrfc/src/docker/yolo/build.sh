#!/bin/bash

# Builds the receive Docker container

docker buildx build --pull -t yolo .
docker tag yolo registry.raspi1.lan/yolo
docker push registry.raspi1.lan/yolo
