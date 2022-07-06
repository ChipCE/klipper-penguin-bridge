#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Error : Root required!"
    exit
fi

APP_DIR="/apps/klipperPenguinBridge/"

systemctl stop klipper-penguin-bridge
rm /etc/systemd/system/klipper-penguin-bridge.service
systemctl daemon-reload
rm -rf "$APP_DIR"
echo "Done"