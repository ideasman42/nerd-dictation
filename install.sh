#!/bin/bash

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Move application files
mkdir -p ~/.local/bin
cp nerd-dictation ~/.local/bin/
cp nerd-dictation-ui ~/.local/bin/
cp commands.py ~/.local/bin/

# Move systemd service file
sudo cp nerd-dictation.service /etc/systemd/system/
sudo systemctl enable nerd-dictation.service

echo "Installation complete. Please reboot your system for the changes to take effect."
