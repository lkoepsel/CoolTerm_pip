#!/usr/local/bin/python3
# Disconnect CoolTerm from serial port

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

    # Open the serial port
    if not s.Disconnect(ID):
        print(f"Unable to disconnect CoolTerm")

    sys.exit()


main()
