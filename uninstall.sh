#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root! command：sudo ./install.sh" 1>&2
   exit 1
fi

UNINSTALL_DIR="/opt/klipper-penguin-bridge"

sudo systemctl stop klipper-penguin-bridge.service
sudo rm /etc/systemd/system/klipper-penguin-bridge.service
sudo systemctl daemon-reload
rm -rf "$UNINSTALL_DIR"
echo "Done"