# CoolTerm package for scripting capabilities
## Description
A pip-installable package to provide scripting capability for [CoolTerm](https://freeware.the-meiers.org). By installing via `pip`, one can easily use the scripting capabilities of CoolTerm via *python*.

## Install
### Steps
```bash
# clone the repository
git clone git@github.com:lkoepsel/CoolTerm_pip.git
# change to the directory
cd CoolTerm_pip
# edit CT_connect.py based on your OS (see Edits... below)
# install software
pip install .
```
### CoolTerm Activation
Its desireable to move the focus to *CoolTerm*, once the build system has completed. This allows you to immediately begin interacting with the microcontroller using *CoolTerm*. This program will make the appropriate changes required for activating *CoolTerm* on *macOS* (using *AppleScript*) or on *Windows* (using *pygetwindow*).

# Usage Example
1. **Make sure you turn on "Enable Remote Control Socket" under "Scripting" in the Preferences**. Otherwise, the error "Could not connect to CoolTerm" will indicate that it there is a problem communicating with CoolTerm.
2. Follow the example scripts contained in the CoolTerm documentation, *CoolTerm -> Scripting -> Python -> Examples*

## Connect and Disconnect
My main scripting requirement is to have my editor, *Sublime Text*, disconnect CoolTerm, upload code then reconnect *CoolTerm*. The tools I use are the following:

### Disconnect - `ct_disc`
To disconnect CoolTerm from the serial port, use `ct_disc` in your scripts.

### Connect - `ct_conn`
To disconnect CoolTerm from the serial port, use `ct_conn` in your scripts.

### Sublime Text (ST) Build Automation
Save this file as *Make AVR_C.sublime-build* using Tools -> Build System -> New Build System in **ST**
```json
{
	"cmd": "make",
	"shell_cmd": "ct_disc && make flash && ct_conn",
	"file_regex": "^(..[^:\n]*):([0-9]+):?([0-9]+)?:? (.*)$",
	"selector": "source.makefile",
	"keyfiles": ["Makefile", "makefile"],

	"variants":
	[
		{
			"name": "Flash only",
			"shell_cmd": "ct_disc && make flash && ct_conn"
		},
		{
			"name": "All new",
			"shell_cmd": "make LIB_clean && make clean && make"
		},
		{
			"name": "Clean",
			"shell_cmd": "make clean"
		},
	]
}
```

Save this file as *MicroPython.sublime-build* using Tools -> Build System -> New Build System in **ST**
```json
{
	"shell_cmd": "echo \" Use main to upload to main.py and same to retain filename\" ",

	"variants":
	[
		{
			"name": "CoolTerm main",
			"shell_cmd": "ct_disc && mpremote cp $file :main.py && mpremote reset && ct_conn"
		},
		{
			"name": "CoolTerm same",
			"shell_cmd": "ct_disc && mpremote cp $file :$file_name && mpremote reset && ct_conn"
		}

	]

}
```
