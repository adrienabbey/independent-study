# Creates a Docker container that hosts a MariaDB database for one or more other containers.

# Use Ubuntu 24.04 as the base image:
FROM ubuntu:24.04

# Install MariaDB (as a single command, cleaning up temporary files)
RUN apt-get update && apt-get install -y mariadb && rm -rf /var/lib/apt/lists/*

# TODO: everything else
# - Persistent DB location
# - Securing the DB (user, pass, etc.)
# - Opening ports for external containers
