# Dockerfile to build a container that uses the NRF24L01 to receive files.
# Intended to be run on the project Raspberry Pis.
# Starting with the Python method: https://github.com/nRF24/pyRF24

# Use Ubuntu 24.04 as a base:
FROM ubuntu:24.04

# Set work directory:
WORKDIR /app

# Install requisite packages:
RUN apt-get update && apt-get install python3-pip python3.12-venv -y && rm -rf /var/lib/apt/lists/*

# Create a virtual environment for Python:
RUN python3 -m venv /opt/venv

# Set the virtual environment's path:
ENV PATH="/opt/venv/bin:$PATH"

# Install the required Python packages:
RUN pip3 install --no-cache-dir pyRF24

# Copy code to the container:
# Put this here to avoid having to constantly reinstall Python when rebuilding the container.
COPY receive.py /app

# Run the Python code:
CMD [ "python", "receive.py" ]
