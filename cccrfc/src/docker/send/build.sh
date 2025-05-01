#!/bin/bash

# Builds the receive Docker container

docker buildx build --pull -t send .
