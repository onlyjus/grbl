#!/usr/bin/env python

import serial
import time
import Tkinter as tk


class gui:
    def __init__(self):
        pass

    def connect(self): 
        # Open grbl serial port
        self.serialCon = serial.Serial('/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.2:1.0',9600)

    def openGcode(self):
        # Open g-code file
        self.gcodeFile = open('./gcode_example.txt','r');

    def wakeUp(self):
        # Wake up grbl
        self.serialCon.write("\r\n\r\n")
        time.sleep(2)   # Wait for grbl to initialize 
        self.serialCon.flushInput()  # Flush startup text in serial input

    def streamGcode(self):
        # Stream g-code to grbl
        for line in self.gcodeFile:
            l = line.strip() # Strip all EOL characters for consistency
            s.write(l + '\n') # Send g-code block to grbl
            grbl_out = s.readline() # Wait for grbl response with carriage return

    def closeConnect(self):
        self.serialCon.close()