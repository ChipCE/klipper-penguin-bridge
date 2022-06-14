#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sudo apt-get update
sudo apt-get install net-tools python3 python3-pip python3-venv

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

yes | sudo cp -rf klipper-penguin-bridge.service /etc/systemd/system/klipper-penguin-bridge.service

sudo systemctl daemon-reload
sudo systemctl start klipper-penguin-bridge
sudo systemctl enable klipper-penguin-bridge
 
