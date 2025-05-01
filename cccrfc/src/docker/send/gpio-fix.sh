#!/bin/bash

# Fixes the GPIO permissions on the Raspberry Pi, allowing container access.

# Add the user to the gpio group:
sudo usermod -aG gpio $USER

# Fix permissions on the GPIO device permanently (from ChatGPT):
echo 'SUBSYSTEM=="bcm2835-gpiomem", GROUP="gpio", MODE="0660"' |
    sudo tee /etc/udev/rules.d/99-gpiomem.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
