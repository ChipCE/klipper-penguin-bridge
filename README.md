# klipper-penguin-bridge

Simple tool to execute linux command and store result into klipper gcode variables

## Theory of operation

- The program execute commands in <code>config.json</code> every <code>updateInterval</code> seconds.(String command must have slash escape.)
- The executed command result will be set to <code>KLIPPER_PENGUIN_BRIDGE</code> macro variable using moonraker restAPI
- Saved variables can be accessed inside kipper with <code>printer["gcode_macro KLIPPER_PENGUIN_BRIDGE"].{VARIABLENAME}</code>

## Requirement

- Python3, python3-pip, python3-venv

<pre> sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
</pre>

## Install

- Add <code>[include klipper_penguin_bridge.cfg]</code> into your <code>printer.cfg</code>
- Edit <code>src/klipper_penguin_bridge.cfg</code> file, add the variable name you need
- Edit <code>src/config.json</code> file, add config for above variables and commands

<pre>
cd 
git clone https://github.com/ChipCE/klipper-penguin-bridge
cd klipper-penguin-bridge
chmod +x install.sh
./install.sh
</pre>
