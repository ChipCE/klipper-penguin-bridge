# klipper-penguin-bridge

Simple tool to execute linux command and store result into klipper variables

## Theory of operation

- The program execute commands in <code>config.json</code> every <code>updateInterval</code> seconds then compare the executed result string with saved variable value.
- If executed result string is not the same as saved variable value, update it via moonraker api with <code>SAVE_VARIABLE</code> command.
- Saved variables can be accessed inside kipper with <code>printer.save_variables.variables.VARIABLENAME</code>

## Requirement

- Add the following macro into klipper config file, replace <code>YOUR_VARIABLE_NAME_HERE</code> with the name of the variable will be used.
<pre>[gcode_macro GLOBAL_VAR]
variable_YOUR_VARIABLE_NAME_HERE : False
variable_YOUR_VARIABLE_NAME_HERE : 69.4
variable_YOUR_VARIABLE_NAME_HERE : "string type data"
gcode:
    </pre>

## Install

<pre>
cd 
git clone https://github.com/ChipCE/klipper-lunar-penguin
cd klipper-penguin-bridge
chmod +x install.sh
./install.sh
</pre>
