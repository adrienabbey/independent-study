# Docker Containers

These are some notes for how our images are built and managed.

## Building the Docker Containers

- CD into the relevant container directory.
- Run `docker build -t containerName .`
  - This will build a docker image for the image in this directory, using the name "containerName"
- To run this Docker image in the background, use: `docker run -d containerName`
  - Note: as of the time of this writing, this is NOT yet working.
- To run the container interactively (for troubleshooting) use: `docker run -it containerName /bin/bash`

## The SPI to USB Adapters

- The SPI to USB adapters use the [FT232H chipset](https://www.digikey.com/htmldatasheets/production/821191/0/0/1/ft232h.pdf).
- To use these adapters at full speed, I need to disable kernel drivers so that I can access them directly. (see MPSSE notes below)
- I then need to pass the adapter into the containers using the USB bus/port numbers. This is done using a Bash script.

### MPSSE and Linux Kernel Drivers

- MPSSE is hardware on the FT232H USB adapter that allows for offloading much of the data transfer processing to the hardware. This allows for faster data transfer. However, to make use of this, we must disable a Linux kernel driver for the FTDI chip.
- To do this, we must create the `/etc/modprobe.d/blacklist-ftdi.conf` file **on the host system, not inside the container** and add the following lines:

```text
blacklist ftdi_sio
blacklist usbserial
```

- Reboot after editing the file to enable the changes.

## Raspberry Pi SPI

- Note that the Raspberry Pi devices need to have their SPI interfaces enabled. This involved installing and using the `raspi-config` tool to enable the interface, then rebooting.
