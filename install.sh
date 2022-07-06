#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Error : Root required!"
    exit
fi

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="/apps/klipperPenguinBridge/"
KLIPPER_CONFIG_DIR="/home/pi/klipper_config/"
KLIPPER_USER="pi"

cd "$CURRENT_DIR"

# install requirements
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# make install dir if not exist
mkdir -p "$APP_DIR"

# copy files over
yes | cp -R "src/klipper-penguin-bridge.py" "$INSTALL_DIR"
yes | cp -R "src/config.json" "$INSTALL_DIR"
yes | cp -R "src/klipper_penguin_bridge.cfg" "$KLIPPER_CONFIG_DIR"
# change file permission
chown $KLIPPER_USER "$KLIPPER_CONFIG_DIR/klipper_penguin_bridge.cfg"
# copy python requirements
yes | cp -R "requirements.txt" "$APP_DIR"
# copy service file
yes | cp -R klipper-penguin-bridge.service /etc/systemd/system/klipper-penguin-bridge.service

# make python venv ans install requirements
cd "$APP_DIR"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# start service
systemctl daemon-reload
systemctl start klipper-penguin-bridge.service
systemctl enable klipper-penguin-bridge.service
systemctl status klipper-penguin-bridge.service



 
