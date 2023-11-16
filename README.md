# CoolTerm package for scripting capabilities
## Description
A pip-installable package to provide scripting capability for [CoolTerm](https://freeware.the-meiers.org).

## Install
Clone this repository locally then 
```bash
cd CoolTerm_pip
pip install .
```
### Automating focus on CoolTerm on exit
Its desireable to move the focus from Sublime Text to CoolTerm, once the build system has completed. This will allow you to immediately begin interacting with the microcontroller using CoolTerm.

Enabling this requires editing *CT_connect.py*. Follow the comments as to which OS you are using. One is for macOS and the other is for Windows. Uncomment only the python code for **either (not both)** sections based on your OS. And comment out the code for the *"other"* OS, for example, comment out macOS code, if uncommenting the Windows code.

# Usage Example
1. Make sure you turn on "Enable Remote Control Socket" under "Scripting" in the Preferences. Otherwise, the error "Could not connect to CoolTerm" will indicate that it there is a problem communicating with CoolTerm.
2. Follow the example scripts contained in the CoolTerm documentation, CoolTerm -> Scripting -> Python -> Examples

## Connect and Disconnect
My main scripting requirement is to have my editor, *Sublime Text*, disconnect CoolTerm, upload code then reconnect CoolTerm. The tools I use are the following:

### Disconnect
To disconnect CoolTerm from the serial port, use `ct_disc` in your scripts.

### Connect
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
