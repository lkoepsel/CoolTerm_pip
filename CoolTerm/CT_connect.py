#!/usr/local/bin/python3
# Connect CoolTerm to serial port

from CoolTerm import CoolTermSocket
import pygetwindow as gw
import pyautogui
import re
import subprocess
import sys
import time


def main():
    s = CoolTermSocket()
    stc = re.compile(r'.*.stc$')
    sys.stdout.reconfigure(encoding='utf-8')

    # Get a list of all visible windows
    windows = gw.getAllTitles()

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

    # uncomment out line below if running on macOS, this will move focus
    # to CoolTerm on exit
    # subprocess.run(["osascript", "-e",
    #                 'tell application "CoolTerm" to activate'])
    # end macOS

    # uncomment out lines below if running on Windows, this will move focus
    # to CoolTerm on exit
    for w in windows:
        if stc.match(w):
            window = gw.getWindowsWithTitle(w)[0]

            # Activate the window
            window.activate()
            print(f"{w} found, CoolTerm activated")
            break

    # end Windows

    sys.exit()


main()
