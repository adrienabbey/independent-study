#!/usr/bin/env python3
"""
nRF24L01 Sender - Team 9
Sends files to a paired nRF24L01+ receiver using dynamic payloads
"""

import os
import sys
import time
from pyrf24 import RF24, RF24_PA_LOW, rf24_datarate_e

# --- CONFIGURATION ---
CE_PIN = 22
CSN_PIN = 0  # CE0
PIPE_ADDRESS = b"Node1"
WIRELESS_CHANNEL = 125
CHUNK_SIZE = 32
RETRY_DELAY = 0.005

# --- SETUP RADIO ---
radio = RF24(CE_PIN, CSN_PIN)
radio.begin()
radio.setChannel(WIRELESS_CHANNEL)
radio.setPALevel(RF24_PA_LOW)
radio.setDataRate(rf24_datarate_e.RF24_1MBPS)
radio.set_auto_ack(True)
radio.setRetries(delay=5, count=15)
radio.enableDynamicPayloads()
radio.openWritingPipe(PIPE_ADDRESS)
radio.stopListening()


def send_packet(data: bytes, retries: int = 3):
    for attempt in range(1, retries + 1):
        success = radio.write(data)
        print(f"[WRITE] Attempt {attempt}: {'OK' if success else 'FAIL'} - {data!r}")
        if success:
            return True
        time.sleep(RETRY_DELAY)
    print("WARNING: Packet failed after retries:", data)
    return False


def send_file(filename):
    header = b"FILEHDR:" + filename.encode("utf-8", errors="ignore")
    send_packet(header)

    with open(filename, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            send_packet(chunk)
            time.sleep(RETRY_DELAY)

    send_packet(b"FILEDONE")


def send_multiple(files_to_send):
    for fname in files_to_send:
        if not os.path.isfile(fname):
            print(f"Error: {fname} is not a valid file.")
            continue
        print(f"Sending file: {fname}")
        send_file(fname)
        print(f"Finished sending {fname}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sender.py <file1> [file2 ...]")
        sys.exit(1)

    files = sys.argv[1:]
    print("Starting sender...")
    send_multiple(files)
    print("Done!")
