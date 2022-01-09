#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root! command：sudo ./install.sh" 1>&2
   exit 1
fi

INSTALL_DIR="/opt/klipper-penguin-bridge"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$SCRIPT_DIR"

sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

sudo mkdir -p "$INSTALL_DIR"
yes | cp -rf src/klipper-penguin-bridge.py "$INSTALL_DIR"/klipper-penguin-bridge.py
yes | cp -rf src/requirements.txt "$INSTALL_DIR"/requirements.txt
yes | cp -rf src/klipper-penguin-bridge.service /etc/systemd/system/klipper-penguin-bridge.service

cd "$INSTALL_DIR"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

sudo systemctl daemon-reload
sudo systemctl start klipper-penguin-bridge.service
sudo systemctl enable klipper-penguin-bridge.service
 
