#!/bin/bash
sudo systemctl stop klipper-penguin-bridge
sudo rm /etc/systemd/system/klipper-penguin-bridge.service
sudo systemctl daemon-reload
echo "Done"