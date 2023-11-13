# CoolTerm package for scripting capabilities
## Description
A pip-installable package to provide scripting capability for [CoolTerm](https://freeware.the-meiers.org).

## Install
Clone this repository locally then 
```bash
cd CoolTerm_pip
pip install .
```

# Usage Example
1. Make sure you turn on "Enable Remote Control Socket" under "Scripting" in the Preferences. Otherwise, the error "Could not connect to CoolTerm" will indicate that it there is a problem communicating with CoolTerm.
2. Follow the example scripts contained in the CoolTerm documentation, CoolTerm -> Scripting -> Python -> Examples

## Connect and Disconnect
My main scripting requirement is to have my editor, *Sublime Text*, disconnect CoolTerm, upload code then reconnect CoolTerm. The tools I use are the following:

### CT_disconnect
Save this file in your prefered executable folder, mine is `~/.local/bin`, make sure it is in your PATH for Sublime Text to find it.
```python
#!/usr/local/bin/python3
# Will disconnect CoolTerm from serial port


from CoolTerm import CoolTermSocket
s = CoolTermSocket()

# Check if there are any open windows
count = s.WindowCount()

if count > 0:
    # Get the ID of the frontmost open window
    ID = s.GetFrontmostWindow()
else:
    print(f"Unable to find a CoolTerm Window, is one open?")

# Open the serial port
if not s.Disconnect(ID):
    print(f"Unable to disconnect CoolTerm")
```

### CT_connect
Save this file in your prefered executable folder, mine is `~/.local/bin`, make sure it is in your PATH for Sublime Text to find it.
```python
#!/usr/local/bin/python3
# Will connect CoolTerm to serial port

import time
import subprocess
import sys
from CoolTerm import CoolTermSocket
s = CoolTermSocket()

# Check if there are any open windows
count = s.WindowCount()

if count > 0:
    # Get the ID of the frontmost open window
    ID = s.GetFrontmostWindow()

# Open the serial port

t = 0
while not s.Connect(ID):
    t += 1
    time.sleep(.1)
    if t > 30:
        print(f"Unable to find/connect to CoolTerm {t / 10} secs")
        sys.exit()
print(f"Connected {t / 10} secs")

# comment out line below if not running on macOS
subprocess.run(["osascript", "-e", 'tell application "CoolTerm" to activate'])
```

### Sublime Text (ST) Build Automation
Save this file as *Make AVR_C.sublime-build* using Tools -> Build System -> New Build System in **ST**
```json
{
	"cmd": "make",
	"shell_cmd": "CT_disconnect.py && make flash && CT_connect.py && osascript -e 'tell application \"CoolTerm\" to activate'",
	"file_regex": "^(..[^:\n]*):([0-9]+):?([0-9]+)?:? (.*)$",
	"selector": "source.makefile",
	"keyfiles": ["Makefile", "makefile"],

	"variants":
	[
		{
			"name": "Flash only",
			"shell_cmd": "CT_disconnect.py && make flash && CT_connect.py"
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
			"shell_cmd": "CT_disconnect.py && mpremote cp $file :main.py && mpremote reset && CT_connect.py"
		},
		{
			"name": "CoolTerm same",
			"shell_cmd": "CT_disconnect.py && mpremote cp $file :$file_name && mpremote reset && CT_connect.py"
		}

	]

}
```
