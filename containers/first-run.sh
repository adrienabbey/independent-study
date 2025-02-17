#!/bin/bash

# This bash script is intended to launch my growing stack of Docker containers.
# TODO: Make this script idempotent.
#   - Don't create a network if it already exists.
#   - Recognize and use existing images.
# NOTE: This is NOT good for long-term maintenance.
#   - I'm creating images from the command line, rather than using a Dockerfile.

# Create a network for my containers to use:
docker network create my-network

# Create a Docker volume for persistent storage:
docker volume create mariadb_data
docker volume create mediawiki_data

# Run the MariaDB container:
docker run -d \
  --name my_mariadb \
  --net my-network \
  -e MARIADB_ROOT_PASSWORD=my-secret-pw \
  -e MARIADB_DATABASE=my_app_db \
  -e MARIADB_USER=my_user \
  -e MARIADB_PASSWORD=$(cat mariadb/.mariadb_password) \
  -v mariadb_data:/var/lib/mysql \
  mariadb:latest
