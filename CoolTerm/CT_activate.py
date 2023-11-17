#!/usr/local/bin/python3
# Connect CoolTerm to serial port and activate CoolTerm on exit
# Follow comments based on OS, be sure to comment the other
# OS sections, as in comment out macOS if running on Windows

import time
from CoolTerm import CoolTermSocket


def actv():
    s = CoolTermSocket()
    ID = s.GetFrontmostWindow()
    s.SetFrontmostWindow(ID, True)
    time.sleep(.5)
    s.Close()
