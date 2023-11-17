#!/usr/local/bin/python3
# Connect CoolTerm to serial port and activate CoolTerm on exit
# Follow comments based on OS, be sure to comment the other
# OS sections, as in comment out macOS if running on Windows

import sys
import time
from CoolTerm import CoolTermSocket


s = CoolTermSocket()

def activate():
    ID = s.GetFrontmostWindow()
    s.SetFrontmostWindow(0, True)
    time.sleep(1)
