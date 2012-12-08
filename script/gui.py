#!/usr/bin/env python
#Python 2.7

import serial
import time
import Tkinter as tk
import ttk
import glob


class gui:
    def __init__(self, parent):
        parent.geometry("250x150+300+300")
        parent.title('grbl gui')

        #create a button bar to change modes
        self.modeButtonBar=tk.Frame(parent, relief=tk.RAISED, bd=2)
        self.modeButtonBar.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        tk.Button(self.modeButtonBar, text='E-Stop', command=self.eStop, bg='red',width=10).pack(fill=tk.X, expand=True)
        ttk.Button(self.modeButtonBar, text='Setup', command=self.setupShow,width=10).pack(fill=tk.X, expand=True)

        #create a frame to show modes
        self.modeFrame=tk.Frame(parent,relief=tk.RAISED, bd=2)
        self.modeFrame.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        self.setupMode()

        #create a frame to show machine graphics
        self.graphics=tk.Frame(parent,relief=tk.RAISED, bd=2)
        self.graphics.pack(side=tk.LEFT, expand=True, fill=tk.Y)

    def findSerialPorts(self):
        self.grblDeviceCombo['values']=glob.glob('/dev/serial/by-id/*')+glob.glob('/dev/tty*')

    def setupMode(self):
        self.setupModeFrame=tk.Frame(self.modeFrame)
        ttk.Label(self.setupModeFrame, text='Select grbl Hardware:').pack()
        self.grblDeviceCombo=ttk.Combobox(self.setupModeFrame, values=self.setupModeFrame)
        self.grblDeviceCombo.pack()

    def setupShow(self):
        self.findSerialPorts()
        self.setupModeFrame.pack(expand=True, fill=tk.BOTH)

    def eStop(self):
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

if __name__ == '__main__':
    root = tk.Tk()
    app=gui(root)
    root.mainloop()
