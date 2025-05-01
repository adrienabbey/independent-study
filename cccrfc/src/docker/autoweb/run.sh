#!/bin/bash

# Bash file to run the Docker image after it's been built.
# This is important to pass each of the USB devices into the container properly.

docker run -it autoweb /bin/bash
