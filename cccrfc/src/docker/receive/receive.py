#!/usr/bin/env python3
"""
nRF24L01 Receiver - Team 9
Receives files from a paired nRF24L01+ sender using dynamic payloads
"""

import os
import time
from pyrf24 import RF24, RF24_PA_LOW, rf24_datarate_e

# --- CONFIGURATION ---
CE_PIN = 22
CSN_PIN = 0  # CE0
PIPE_ADDRESS = b"Node1"
WIRELESS_CHANNEL = 125
MAX_PAYLOAD_SIZE = 32

# --- SETUP RADIO ---
radio = RF24(CE_PIN, CSN_PIN)
radio.begin()
radio.setChannel(WIRELESS_CHANNEL)
radio.setPALevel(RF24_PA_LOW)
radio.setDataRate(rf24_datarate_e.RF24_1MBPS)
radio.set_auto_ack(True)
radio.setRetries(delay=5, count=15)
radio.enableDynamicPayloads()
radio.openReadingPipe(1, PIPE_ADDRESS)
radio.openWritingPipe(PIPE_ADDRESS)  # Required for ACKs
radio.startListening()
radio.flush_rx()


def receive_file_chunks():
    current_file = None
    current_filename = None

    print("Receiver ready, listening for files...")

    while True:
        while radio.available():
            payload_size = radio.getDynamicPayloadSize()
            if payload_size == 0:
                radio.flush_rx()
                continue
            elif payload_size > MAX_PAYLOAD_SIZE:
                print(f"WARNING: Oversized packet ({payload_size}), discarding.")
                radio.read(payload_size)
                continue

            payload = radio.read(payload_size)
            print(f"[RECV] {payload_size} bytes: {payload!r}")

            if payload.startswith(b"FILEHDR:"):
                if current_file:
                    current_file.close()
                filename = payload[len(b"FILEHDR:") :].decode("utf-8", errors="ignore")
                current_filename = filename
                current_file = open(filename, "wb")
                print(f"Receiving new file: {filename}")

            elif payload == b"FILEDONE":
                if current_file:
                    current_file.close()
                    print(f"File transfer complete: {current_filename}")
                    current_file = None
                    current_filename = None
                else:
                    print("WARNING: Received FILEDONE with no open file.")

            else:
                if current_file:
                    current_file.write(payload)
                else:
                    print("WARNING: Data received with no file open.")

        time.sleep(0.001)


if __name__ == "__main__":
    try:
        receive_file_chunks()
    except KeyboardInterrupt:
        print("\nExiting...")
