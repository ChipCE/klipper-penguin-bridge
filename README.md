# klipper-penguin-bridge

Simple tool to execute linux command and store result into klipper variables

## Theory of operation

- The program execute commands in <code>config.json</code> every <code>updateInterval</code> seconds. String command must have slash escape.
- Compare the executed result string with saved variable value. If executed result string is not the same as saved variable value, update it via moonraker api with <code>SAVE_VARIABLE</code> command.
- Saved variables can be accessed inside kipper with <code>printer.save_variables.variables.VARIABLENAME</code>

## Requirement

- Python3
- Enable <code>save_variables</code> in klipper config.

## Install

<pre>
cd 
git clone https://github.com/ChipCE/klipper-penguin-bridge
cd klipper-penguin-bridge
chmod +x install.sh
./install.sh
</pre>
