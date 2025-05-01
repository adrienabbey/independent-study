# Dockerfile for image recognition using Jamal's code.

# Use Ubuntu 24.04 as a base:
FROM ubuntu:24.04

# Set working directory:
WORKDIR /app

# Install requisite packages:
RUN apt-get update && \
    apt-get install python3-pip python3.12-venv libftdi1-2 curl unzip git libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 -y && \
    rm -rf /var/lib/apt/lists/*

# Create the virtual environment for Python:
RUN python3 -m venv /opt/venv

# Set the virtual environment's path:
ENV PATH="/opt/venv/bin:$PATH"

# Install the required Python packages:
RUN pip3 install --no-cache-dir ultralytics

# Copy code to the container:
COPY . /app

# Run the Python code:
CMD [ "python", "deathStarReceognition.py" ]
