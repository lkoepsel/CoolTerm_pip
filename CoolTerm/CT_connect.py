#!/usr/local/bin/python3
# Connect CoolTerm to serial port and activate CoolTerm on exit
# Follow comments based on OS, be sure to comment the other
# OS sections, as in comment out macOS if running on Windows

import sys
import time
from CoolTerm import CoolTermSocket
import platform

OS = platform.system()
if OS == "Windows":
    import pygetwindow as gw
    # import pyautogui
    import re

if OS == "Darwin":
    import subprocess


def conn():
    s = CoolTermSocket()

    # Windows uncomment next 2 lines
    if OS == "Windows":
        stc = re.compile(r'.*.stc')
        untitled = re.compile(r'.*Untitled.*')
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

    # Move focus to CoolTerm
    # macOS uncomment next 1 line below
    if OS == "Darwin":
        subprocess.run(["osascript", "-e",
                        'tell application "CoolTerm" to activate'])
    # end macOS

    # Windows uncomment next 6 lines
    if OS == "Windows":
        for w in windows:
            if stc.match(w) or untitled.match(w):
                window = gw.getWindowsWithTitle(w)[0]
                window.activate()
                print(f"Window {w} found, CoolTerm activated")
                break
        # end Windows
    s.Close()
