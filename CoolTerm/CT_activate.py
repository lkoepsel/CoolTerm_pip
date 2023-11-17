#!/usr/local/bin/python3
# Connect CoolTerm to serial port and activate CoolTerm on exit
# Follow comments based on OS, be sure to comment the other
# OS sections, as in comment out macOS if running on Windows

import sys
import time
from CoolTerm import CoolTermSocket


def main():
    s = CoolTermSocket()
    ID = s.GetFrontmostWindow()
    s.SetFrontmostWindow(ID, True)
    sys.exit()


main()
