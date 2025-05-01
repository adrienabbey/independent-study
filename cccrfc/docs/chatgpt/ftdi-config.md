# Tell me more about FT2232H in MPSSE mode.  Assume I'm running Linux and using Python

Using the FT2232H in MPSSE mode on Linux with Python is quite feasible and can be done with libraries such as **pyftdi** (preferred for ease of use) or **libftdi + custom Python bindings**. Below is an overview of how MPSSE works, how to configure the FT2232H under Linux, and an example of using Python (via **pyftdi**) to communicate with an SPI device.

---

## 1. What is MPSSE?

**MPSSE (Multi-Protocol Synchronous Serial Engine)** is a feature in certain FTDI chips (e.g., FT2232H, FT232H, FT4232H) that allows the chip to handle synchronous serial interfaces like **SPI**, **I²C**, or **JTAG** in hardware. Instead of “bit-banging” in software, MPSSE can automatically clock data in and out, significantly reducing overhead and allowing higher bus speeds.

Key points about MPSSE:

- You configure one of the FT2232H’s channels (A or B) as an MPSSE port rather than a traditional UART or bit-bang port.
- Once in MPSSE mode, the FT2232H can perform SPI reads/writes (and optionally other protocols), controlling clock, MOSI, and MISO directly in hardware.
- You can also assign additional GPIO pins for chip-select lines, interrupt lines, reset, etc.

---

## 2. Linux Environment Setup

### 2.1 Driver Considerations

On Linux, you have two main driver paths:

1. **FTDI’s built-in VCP (Virtual COM Port) driver**: This driver turns each channel into a serial port (`/dev/ttyUSBx`). This is *not* what you want for MPSSE mode.  
2. **libusb / libftdi**: A generic USB library plus a specialized library for FTDI chips that lets user-space applications control the FTDI device without the kernel’s VCP driver.  

For MPSSE, you typically have to **detach** or **blacklist** the built-in FTDI kernel driver so you can talk to the device directly via libusb in user space.

#### Blacklisting the Kernel’s FTDI Driver

If your system automatically loads the FTDI VCP driver, you’ll need to prevent that. For example, add a file like `/etc/modprobe.d/blacklist-ftdi.conf`:

```text
blacklist ftdi_sio
blacklist usbserial
```

Then either reboot or manually unload these modules. Once they’re blacklisted/unloaded, tools like **pyftdi** or **libftdi** can claim the device directly via USB.

---

## 3. Python Options

### 3.1 PyFtdi

[**PyFtdi**](https://pypi.org/project/pyftdi/) is a pure Python library (on top of `libusb`) that supports MPSSE operations on FTDI chips. It is often the easiest route if you want a simple, Pythonic interface.

Features:

- No compiling or special driver needed (just the `libusb` system library).
- Provides an SPI interface, an I2C interface, as well as general GPIO methods.

Install it via:

```bash
pip install pyftdi
```

### 3.2 libftdi with Python Bindings

Another option is [**libftdi**](https://www.intra2net.com/en/developer/libftdi/) plus Python bindings (e.g., [pylibftdi](https://pypi.org/project/pylibftdi/)). This is a bit more “manual” but still a valid choice. PyFtdi tends to be more straightforward for SPI, so we’ll focus on pyftdi here.

---

## 4. Configuring and Using MPSSE with PyFtdi

Below is a **quick-start** guide for SPI mode using `pyftdi`:

### 4.1 Basic Connection Example

Assume you have:

- **FT2232H** with channel A configured at runtime in MPSSE mode by PyFtdi.
- An SPI slave device (e.g., an nRF24L01) connected to the FT2232H’s ADBUS pins for MOSI, MISO, SCK, and a GPIO for chip select.

**Pin assignment** in PyFtdi’s default SPI “pin out” for a single FTDI interface typically looks like this:

| FT2232/FT232 Pin | MPSSE Function | PyFtdi default usage |
|------------------|----------------|----------------------|
| ADBUS0          | SCK            | SPI clock            |
| ADBUS1          | MOSI           | SPI MOSI             |
| ADBUS2          | MISO           | SPI MISO             |
| ADBUS3          | GPIO (CS)      | Often used for CS0   |
| ADBUS4,5,6,7    | GPIO           | Additional GPIOs     |

> **Tip**: By default, PyFtdi tries to use ADBUS3 as the first chip select line (CS0), but you can configure more lines.

### 4.2 Finding the Right FTDI URL

PyFtdi devices are addressed with a “URL” of the form:

```text
ftdi://<vendor>:<product>/<serial or index>
```

- `<vendor>:<product>` are the USB VID:PID (by default FTDI’s is `0403:6010` for the FT2232H).  
- You can omit them if you only have a single FTDI device or use `ftdi://::/1` which means “use the first FTDI device’s interface 1.”  
- Typically, “/1” would mean “interface 1” (channel A), and “/2” would mean “interface 2” (channel B).  

### 4.3 Sample Python SPI Code

Here’s a minimal Python script using **pyftdi** to initialize SPI on channel A (interface 1), set up an 8 MHz SPI clock, and perform a simple transaction:

```python
#!/usr/bin/env python3

from pyftdi.spi import SpiController

def main():
    # Create an SPI controller
    spi = SpiController()

    # Configure the first interface of the first FT2232H in MPSSE mode
    # This is typically channel A on a FT2232H device
    # The URL 'ftdi://ftdi:2232h/1' might also be used specifically
    spi.configure('ftdi://::/1')

    # Get a port to a specific slave (device) with chip-select 0
    # mode=0 => SPI mode 0 (CPOL=0, CPHA=0)
    # max_hz=8E6 => 8 MHz
    slave = spi.get_port(cs=0, freq=8E6, mode=0)

    # Write some bytes [0x9F] and read back 3 bytes simultaneously
    # Example: an SPI FLASH "Read ID" command, but we can adapt for nRF24
    response = slave.exchange([0x9F], 3)
    print("Received bytes:", response)

    # De-initialize
    spi.terminate()

if __name__ == '__main__':
    main()
```

#### Notes

- `cs=0` by default maps to ADBUS3 (if you haven’t changed PyFtdi’s pin assignments).  
- You can call `get_gpio()` if you need to manipulate separate GPIO lines (e.g., for nRF24 **CE** pin).  
- For the nRF24, you’ll typically do `slave.exchange([RegisterWriteCommand, Value], length_of_response)` calls, toggling CE via GPIO, etc.

---

## 5. Handling Additional GPIO (for CE, IRQ, etc.)

When using SPI to interface with a device like the **nRF24L01**, you need at least two additional lines:

1. **CE**: Chip Enable (not the same as SPI chip select). This is driven high or low to enter TX or RX modes.  
2. **IRQ** (optional): An interrupt line from the nRF24 to signal TX/RX completion.

With PyFtdi, after you’ve configured the SPI interface, you can retrieve the raw GPIO port of the same MPSSE interface:

```python
from pyftdi.spi import SpiGpioPort

# after spi.configure(...)
# the SPI port itself uses ADBUS0..2 for SCK, MOSI, MISO, and ADBUS3 for CS
# Suppose you want to use ADBUS4 for CE, and ADBUS5 for IRQ.

gpio = spi.get_gpio()

# Configure ADBUS4 (bit 4) as output (CE), ADBUS5 (bit 5) as input (IRQ)
# The bits are 0..7 for ADBUS0..7 in the default mapping
direction_mask = 0b00010000  # bit4 = 1 for output, bit5 = 0 for input
gpio.set_direction(direction_mask)

# Set CE high (bit4 = 1 => 0b00010000)
gpio.write(0b00010000)

# To read IRQ (bit5), just read the GPIO pins:
pins = gpio.read()
irq_level = (pins >> 5) & 1
print("IRQ pin is at level:", irq_level)
```

You’d repeat these reads and writes in your Python code as needed to control CE or detect IRQ changes.

---

## 6. Tips & Common Pitfalls

1. **Ensure the FT2232H is powered at 3.3 V (VCCIO) if your SPI device is 3.3 V**. The FT2232H can handle 1.8–3.3 V I/O if configured properly, but *never apply 5 V to nRF24L01 lines*.
2. **Blacklisting kernel drivers**: Make sure the `ftdi_sio` driver does not bind to the device.  
3. **Selecting the correct interface**: The FT2232H has two interfaces (A and B). Use `ftdi://::/1` for the first interface, `ftdi://::/2` for the second, or specify the device’s serial.  
4. **SPI Mode**: nRF24L01 typically uses SPI mode 0 (CPOL=0, CPHA=0). Ensure `mode=0`.  
5. **Speed**: The nRF24L01 typically supports up to 10 MHz SPI, but always start at a moderate speed (e.g., 2–4 MHz) and increase if everything is stable.  
6. **Interrupt Handling**: If you need immediate handling of an IRQ, remember that PyFtdi is still user-space polling. You can poll the GPIO input or read the IRQ status from the nRF24’s status register directly over SPI. True hardware interrupts are not supported by the FTDI chip in the same way a microcontroller would handle them.

---

## 7. Summary

- **MPSSE** is a hardware engine in the FT2232H that directly handles SPI/I²C/JTAG, offloading bit-banging from software.
- On Linux, use **pyftdi** (or libftdi) in Python to configure MPSSE mode, set SPI parameters, and communicate with your device.
- For **nRF24L01**, you’ll use SPI lines plus extra GPIO (CE, IRQ) to fully control the transceiver.
- Pyftdi provides a straightforward, high-level Python API for SPI transfers and GPIO manipulation, making it ideal for quick prototyping and testing.

With these steps, you can confidently set up your FT2232H on Linux, switch it into MPSSE mode from Python, and start sending SPI commands to your target device (like the nRF24L01 or any other SPI peripheral).
