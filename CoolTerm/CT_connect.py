#!/usr/local/bin/python3
# Connect CoolTerm to serial port

import time
import subprocess
import sys
from CoolTerm import CoolTermSocket


def main():
    s = CoolTermSocket()

    # Check if there are any open windows
    count = s.WindowCount()

    if count > 0:
        # Get the ID of the frontmost open window
        ID = s.GetFrontmostWindow()
    else:
        print(f"Unable to find a CoolTerm Window, is one open?")
        sys.exit()

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
    subprocess.run(["osascript", "-e",
                    'tell application "CoolTerm" to activate'])
    sys.exit()


main()
