# Dockerfile for Isaak's web server:

# Use Ubuntu 24.04 as a base:
FROM ubuntu:24.04

# Set working directory:
WORKDIR /app

# Install requisite packages:
RUN apt-get update && \
    apt-get install python3-pip python3.12-venv curl tmux -y && \
    rm -rf /var/lib/apt/lists/*

# Create the virtual environment for Python:
RUN python3 -m venv /opt/venv

# Set the virtual environment's path:
ENV PATH="/opt/venv/bin:$PATH"

# Install the required Python packages:
RUN pip3 install --no-cache-dir Flask

# Install Ngrok:
RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | tee /etc/apt/sources.list.d/ngrok.list \
    && apt update \
    && apt install ngrok

# Add ngrok API key:
RUN ngrok config add-authtoken REPLACE_ME

# Copy code to the container:
COPY . /app

# Run the Python code:
CMD [ "python", "script.py" ]
