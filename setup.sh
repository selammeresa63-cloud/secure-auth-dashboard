#!/bin/bash

echo "=== System Packages Installation ==="
sudo apt update
sudo apt install -y python3-pip python3-venv git

echo "=== Virtual Environment Setup ==="
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo "=== Installing Python Dependencies ==="
pip install -r requirements.txt

echo "=== Setup Complete! ==="
echo "To activate virtual environment run: source venv/bin/activate"
