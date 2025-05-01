Below is an outline of how to transfer a file using **pyRF24** in Python, which is a wrapper around TMRh20’s popular RF24 C++ library. The overall process is similar to the C++ approach—chunk the file, send packets, and handle reading/reassembling on the other side—but in Python you’ll use the **pyRF24** module to talk to the nRF24L01 via SPI.

---

1. Installation and Setup

---

1. **Enable SPI** on your Raspberry Pi’s Ubuntu host (outside Docker).

   - Edit or create **/boot/firmware/config.txt** (or the corresponding place for Ubuntu on Pi) and add:
     ```
     dtparam=spi=on
     ```
   - Reboot the Pi (`sudo reboot`) and verify that `/dev/spidev0.0` (and possibly `/dev/spidev0.1`) exist.

2. **Docker container** privileges / device mapping.

   - Easiest: run the container in privileged mode:
     ```bash
     docker run -it --privileged your_image_name /bin/bash
     ```
   - More secure: pass only the SPI device and GPIO interface into the container:
     ```bash
     docker run -it \
       --device /dev/spidev0.0 \
       --device /dev/gpiomem \
       your_image_name /bin/bash
     ```
   - Either way, confirm from inside the container that `/dev/spidev0.0` is visible.

3. **Install pyRF24** inside the container.
   - If there’s a PyPI package for your environment, try:
     ```bash
     pip install pyRF24
     ```
   - If not available/precompiled, you may need to clone and build from source. For example:
     ```bash
     apt-get update && apt-get install -y git build-essential python3-dev
     git clone https://github.com/marcosawrey/pyRF24.git
     cd pyRF24
     # Edit the setup.py or environment variables if needed (CE/CSN pins).
     python3 setup.py build
     python3 setup.py install
     ```
     This will compile and install the Python wrapper, assuming the underlying TMRh20/RF24 C++ library builds successfully.

---

2. Wiring Recap

---

**nRF24L01** → **Raspberry Pi 4**

- VCC → 3.3 V
- GND → GND
- CE → a free GPIO, e.g. GPIO 22 (physical pin 15)
- CSN → SPI CE0 (physical pin 24)
- SCK → SPI SCLK (physical pin 23)
- MOSI → SPI MOSI (physical pin 19)
- MISO → SPI MISO (physical pin 21)

---

3. Basic pyRF24 Usage

---

**Minimal transmitter example** (send “Hello World”):

```python
#!/usr/bin/env python3
import time
from RF24 import RF24, RF24_PA_LOW

# CE pin = GPIO22, CSN = SPI0 CE0 => bus=0, device=0
# On the Pi, CE GPIO pin is 22, the SPI device is 0
radio = RF24(22, 0)

# An nRF24 address is typically 5 bytes
address = b"1Node"

def setup_radio():
    # Start the radio
    if not radio.begin():
        raise OSError("radio hardware not responding")

    radio.setPALevel(RF24_PA_LOW)      # RF24_PA_MIN, _LOW, _HIGH, _MAX
    radio.setChannel(108)             # e.g. 2.508 GHz (2400 + 108 MHz)
    radio.setDataRate(radio.BR_1MBPS) # 250K, 1M, or 2M
    radio.setRetries(5, 15)           # delay, count
    radio.openWritingPipe(address)
    radio.stopListening()             # set as transmitter

def transmit_message(msg):
    result = radio.write(msg)
    if result:
        print(f"Sent: {msg}")
    else:
        print("Send failed!")

if __name__ == "__main__":
    setup_radio()

    while True:
        transmit_message(b"Hello World!")
        time.sleep(1.0)
```

**Minimal receiver example**:

```python
#!/usr/bin/env python3
import time
from RF24 import RF24, RF24_PA_LOW

radio = RF24(22, 0)
address = b"1Node"

def setup_radio():
    if not radio.begin():
        raise OSError("radio hardware not responding")

    radio.setPALevel(RF24_PA_LOW)
    radio.setChannel(108)
    radio.setDataRate(radio.BR_1MBPS)
    radio.openReadingPipe(1, address)
    radio.startListening()  # set as receiver

if __name__ == "__main__":
    setup_radio()
    while True:
        # If data is ready, read it
        if radio.available():
            received_payload = []
            radio.read(received_payload, radio.getDynamicPayloadSize())
            print("Got:", bytes(received_payload))
        time.sleep(0.1)
```

---

4. Sending a File in Chunks

---

To send a file over nRF24, you must break it into chunks (max 32 bytes per packet in standard config). Then on the receiving side, piece it back together. Below is a simplified approach:

### Transmitter (file-sending) example

```python
#!/usr/bin/env python3
import os
import time
from RF24 import RF24

radio = RF24(22, 0)
address = b"1Node"

CHUNK_SIZE = 32

def setup_radio():
    if not radio.begin():
        raise OSError("radio hardware not responding")
    radio.setPALevel(radio.PA_LOW)
    radio.setChannel(108)
    radio.setDataRate(radio.BR_1MBPS)
    radio.setRetries(5,15)
    radio.openWritingPipe(address)
    radio.stopListening()

def send_file(filename):
    """Send the contents of 'filename' in 32-byte chunks."""
    filesize = os.path.getsize(filename)
    print(f"Sending file: {filename}, size={filesize} bytes")

    # One approach is to send a “header” with the file size
    # so the receiver knows how many bytes to expect.
    header = f"SIZE:{filesize}".encode('utf-8')
    radio.write(header)
    time.sleep(0.05)  # small delay

    with open(filename, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                # When done, send an “EOF” marker
                radio.write(b"EOF")
                print("File send complete.")
                break
            success = radio.write(chunk)
            if not success:
                print("Chunk send failed. You might retry or handle error.")
            # tiny pause to let receiver keep up
            time.sleep(0.01)

def main():
    setup_radio()
    send_file("somefile.bin")

if __name__ == "__main__":
    main()
```

### Receiver (file-saving) example

```python
#!/usr/bin/env python3
import time
from RF24 import RF24

radio = RF24(22, 0)
address = b"1Node"
CHUNK_SIZE = 32

def setup_radio():
    if not radio.begin():
        raise OSError("radio hardware not responding")
    radio.setPALevel(radio.PA_LOW)
    radio.setChannel(108)
    radio.setDataRate(radio.BR_1MBPS)
    radio.openReadingPipe(1, address)
    radio.startListening()

def main():
    setup_radio()

    # We’ll store the expected size after we get the "SIZE:NNN" message
    expected_size = 0
    received_bytes = 0
    out_file = None

    print("Receiver ready...")
    while True:
        if radio.available():
            buffer = bytearray(radio.getDynamicPayloadSize())
            radio.read(buffer, len(buffer))

            # Convert to string for simple “header” detection
            text = buffer.decode('utf-8', errors='ignore')

            # Check for “SIZE:” header
            if text.startswith("SIZE:"):
                expected_size = int(text.split(":")[1])
                print(f"Expecting {expected_size} bytes.")
                # open file for writing
                out_file = open("received_file.bin", "wb")
                received_bytes = 0
                continue

            # If we see “EOF”, we’re done
            if text.startswith("EOF"):
                print("Finished receiving file.")
                if out_file:
                    out_file.close()
                out_file = None
                expected_size = 0
                received_bytes = 0
                continue

            # Otherwise, treat it as file data
            if out_file:
                out_file.write(buffer)
                received_bytes += len(buffer)
                if received_bytes >= expected_size and expected_size != 0:
                    print("Received all expected bytes.")
                    out_file.close()
                    out_file = None
                    expected_size = 0
                    received_bytes = 0
            else:
                # We got data but no file open -> possibly ignore or handle error
                print("Data arrived but no file is open for writing.")

        # Avoid 100% CPU usage
        time.sleep(0.001)

if __name__ == "__main__":
    main()
```

In this approach:

1. **Transmitter** first sends a short header `"SIZE:<length>"`.
2. Then it reads the file in chunks (max 32 bytes) and sends each chunk.
3. On finishing, it sends an `"EOF"` marker.
4. **Receiver** waits for data:
   - If it sees `"SIZE:<N>"`, it opens a local file for writing and notes how many bytes to expect.
   - If it sees `"EOF"`, it closes the file.
   - Otherwise, it writes raw bytes to `received_file.bin`.

Feel free to wrap each data chunk with your own structure (e.g., chunk ID, sequence number) if you need re-tries or advanced reliability. TMRh20’s RF24 does have basic auto-ack for each packet, but for robust large-file transfers you may consider a small, custom “ack and resend” layer or TMRh20’s `RF24Network`.

---

5. Notes and Tips

---

1. **Chunk size**: The nRF24 default is up to 32 bytes per packet (including user payload). If you want dynamic payloads or bigger, ensure both sides use the same maximum.
2. **Power and Decoupling**: nRF24L01 modules can be sensitive to noisy power. Include a 10 µF capacitor from VCC to GND near the module for better stability.
3. **Data Rates**: You can try `radio.setDataRate(radio.BR_250KBPS)` for improved range/reliability, or 1 Mbps / 2 Mbps for speed.
4. **Range**: For better range, consider an nRF24L01+PA+LNA module (with external antenna).
5. **Docker**: If you see “cannot open SPI device” inside Docker, verify you ran with `--device=/dev/spidev0.0` or `--privileged`.
6. **Handling timeouts**: By default, `radio.write()` will block until it’s either successful or times out if auto-ack is used. If you want to re-try or handle partial transmissions, add code to check the returned status and potentially re-send.

---

## Summary

- Install **pyRF24** inside your Docker container.
- Wire the nRF24L01’s CE and SPI pins to the Pi.
- Use `RF24(ce_pin, csn_pin)` in Python, then configure channel, data rate, addresses, etc.
- For **file transfers**, break the file into 32-byte packets, send them in a loop, and reconstruct on the receiver.
- Use basic headers (e.g., “SIZE:” and “EOF”) or your own custom protocol to coordinate.

That’s all! You now have a Python-based approach for sending arbitrary file data via the nRF24L01, using pyRF24 on a Raspberry Pi with Docker.
