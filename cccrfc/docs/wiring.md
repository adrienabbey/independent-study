# Wiring Instuctions

> WORK IN PROGRESS

## Components

### NRF24L01+PA+LNA

- Note: This has TWO parts: the NRF24L01 radio board itself, and a breakout adapter board that attaches to it.
- From the breakout board, the following pins are available:
  - `CE`: Chip Enable. Toggles between standby and active modes.
  - `CSN`: Chip Select Not. Used for SPI communication. When low, communications are enabled. Ignored when high.
  - `SCK`: Serial Clock. Clock for SPI communication.
  - `MOSI`: Master In, Slave Out. Used to receive data from the radio back to the SPI adapter.
  - `MISO`: Master Out, Slave In. Used to send data from the SPI adapter to the the radio.
  - `IRQ`: Interrupt Request. Optional. Used to signal the SPI adapter when certain events occur, such as data received or transmission complete.
  - `VCC`: Power supply. Typically 3.3V
  - `GND`: Ground.

### ~~FT232H~~

## NRF24L01+PA+LNA to Raspberry Pi (send)

![Raspberry Pi GPIO Diagram](GPIO-Pinout-Diagram-2.png)

- Attach the NRF24L01 board to its adapter board.
- Connect the following pins between the adapter board and the Raspberry Pi 4 GPIO pins:
  - NRF24L01 `VCC` -> RasPi `3.3V` (RED)
  - NRF24L01 `GND` -> RasPi `GND` (BLK)
  - NRF24L01 `CE` -> RasPi `GPIO 22 / Pin 15` (VIO)
  - NRF24L01 `CSN` -> RasPi `GPIO SPI0 CE0 / GPIO 8 / Pin 24` (ORG)
  - NRF24L01 `SCK` -> RasPi `GPIO 11 (SCLK) / Pin 23` (YEL)
  - NRF24L01 `MOSI` -> RasPi `GPIO 10 (MOSI) / Pin 19` (BLU)
  - NRF24L01 `MISO` -> RasPi `GPIO 9 (MISO) / Pin 21` (GRY)
  - ~~NRF24L01 `IRQ` -> RasPi `GPIO 24 / Pin 18` (WHT)~~

## ~~NRF24L01+PA+LNA to FT232H (receive)~~

- Time to pivot. The pyFTDI library does not appear to be compatible with the pyRF24 library.
