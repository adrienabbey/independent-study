#!/bin/bash

# Bash file to run the Docker image after it's been built.
# This is important to pass each of the USB devices into the container properly.

docker run -it \
    --device /dev/gpiomem \
    --device /dev/spidev0.0 \
    --device /dev/gpiochip0 \
    send /bin/bash
