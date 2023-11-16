#!/usr/local/bin/python3
# Connect CoolTerm to serial port and activate CoolTerm on exit
# follow comments based on OS, be sure to comment the other
# OS sections, as in comment out macOS if running on Window

import sys
import time
from CoolTerm import CoolTermSocket

# Windows uncomment next 3
# import pygetwindow as gw
# import pyautogui
# import re

# macOS uncomment next 1
import subprocess


def main():
    s = CoolTermSocket()

    # Windows uncomment next 2 lines
    # stc = re.compile(r'.*.stc$')
    # windows = gw.getAllTitles()

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

    # macOS uncomment next 1 line below
    subprocess.run(["osascript", "-e",
                    'tell application "CoolTerm" to activate'])
    # end macOS

    # Windows uncomment next 6 lines
    # for w in windows:
    #     if stc.match(w):
    #         window = gw.getWindowsWithTitle(w)[0]
    #         window.activate()
    #         print(f"{w} found, CoolTerm activated")
    #         break
    # end Windows

    sys.exit()


main()
