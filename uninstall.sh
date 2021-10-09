#!/bin/bash
sudo systemctl stop klipper-lunar-penguin
sudo rm /etc/systemd/system/test.service
sudo systemctl daemon-reload
echo "Done"