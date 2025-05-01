# How do I use the FT232H as an SPI interface on Linux?

You can use the FT232H as an SPI interface on Linux by leveraging libraries that communicate with the chip in MPSSE mode. One of the most popular ways is to use [PyFtdi](https://eblot.github.io/pyftdi/), a pure-Python driver that supports SPI, I²C, and GPIO on FTDI devices.

Below are the steps and an example to get you started:

---

## 1. Install Dependencies

- **Install PyFtdi:**

  ```bash
  pip install pyftdi
  ```

- **Unload the Kernel Driver (if necessary):**

  On many Linux distributions, the built-in `ftdi_sio` kernel module will claim the FT232H, which can prevent PyFtdi from accessing it in MPSSE mode. You may need to unload it temporarily:

  ```bash
  sudo rmmod ftdi_sio
  sudo rmmod usbserial
  ```

  *Tip:* To permanently prevent the module from loading, you can blacklist it by adding `blacklist ftdi_sio` (and `blacklist usbserial` if needed) to a file in `/etc/modprobe.d/`.

---

## 2. Identify Your Device

Use the PyFtdi tool to list connected FTDI devices:

```bash
pyftdi-tool -l
```

This will output device URLs (e.g., `ftdi://ftdi:232h/1`) that you'll use to configure the SPI interface.

---

## 3. Write a Python Script to Use SPI

Below is a basic example that opens the SPI interface, writes data, and reads a response:

```python
from pyftdi.spi import SpiController

# Initialize the SPI controller
spi = SpiController()

# Configure the FT232H device (adjust the URL as needed)
spi.configure('ftdi://ftdi:232h/1')

# Acquire an SPI port:
# - cs=0: Chip select (use a value from 0 to 7 as needed)
# - freq=1E6: Clock frequency (1 MHz in this example)
# - mode=0: SPI mode (CPOL=0, CPHA=0)
slave = spi.get_port(cs=0, freq=1E6, mode=0)

# Example: Send a command (e.g., 0x9F) and read 3 bytes back
data_to_send = bytes([0x9F])
response = slave.exchange(data_to_send, 3)

print("Received:", response)
```

**Explanation:**

- **`spi.configure(...)`** initializes communication with the FT232H. The URL specifies the device; adjust it according to what `pyftdi-tool -l` returns.
- **`spi.get_port(...)`** sets up an SPI port with the desired chip select, frequency, and mode.
- **`slave.exchange(...)`** sends data (here, a single byte command) and reads a specified number of bytes in return.

---

## 4. Run Your Script

Make sure your FT232H is connected and not claimed by other drivers, then run your script:

```bash
python your_spi_script.py
```

---

## Additional Tips

- **Documentation:** Check out the [PyFtdi documentation](https://eblot.github.io/pyftdi/api/spi.html) for more advanced usage and configuration options.
- **Alternative Libraries:** There are other libraries (and even C libraries like libftdi or FTDI’s D2XX drivers) that can work with the FT232H, but PyFtdi is often the simplest and most Pythonic approach.
- **Testing:** If you run into issues, verify that your device URL is correct and that no conflicting drivers are active.

By following these steps, you should be able to use your FT232H as an SPI interface on Linux successfully.
