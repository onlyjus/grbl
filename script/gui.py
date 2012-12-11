#!/usr/bin/env python
#Python 2.7

import serial #pyserial library
import time
import Tkinter as tk
import tkMessageBox as box
import ttk
import glob


class gui:
    def __init__(self, parent):
        parent.geometry("600x400+300+300")
        parent.title('grbl gui')

        #variables
        self.statusButtontext=tk.StringVar()
        self.statusButtontext.set('Enable')
        self.pauseButtontext=tk.StringVar()
        self.pauseButtontext.set('Pause')
        self.grblDevice=tk.StringVar()
        self.grblDevice.set('Select a Device')

        #create a button bar
        self.buttonBar=tk.Frame(parent, relief=tk.RAISED, bd=2)
        self.buttonBar.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        tk.Button(self.buttonBar, text='E-Stop', command=self.eStop, bg='red',width=10, height=5).pack(fill=tk.X, expand=True)
        self.enableButton=tk.Button(self.buttonBar, textvariable=self.statusButtontext, command=self.status, bg='red',width=10, height=5)
        self.enableButton.pack(fill=tk.X, expand=True)
        self.pauseButton=tk.Button(self.buttonBar, textvariable=self.pauseButtontext, command=self.pause,bg='green',width=10, height=5)
        self.pauseButton.pack(fill=tk.X, expand=True)
        tk.Button(self.buttonBar, text='Options',height=5).pack(fill=tk.X, expand=True)

        #create a frame to show controls
        self.controlFrame=tk.Frame(parent,relief=tk.RAISED, bd=2)
        self.controlFrame.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        #device selection
        self.deviceSelFrame=ttk.LabelFrame(self.controlFrame, text='Select grbl Hardware')
        self.deviceSelFrame.pack(pady=5, expand=True, fill=tk.X)
        self.grblDeviceCombo=ttk.Combobox(self.deviceSelFrame, textvariable=self.grblDevice)
        self.grblDeviceCombo.pack(side=tk.LEFT,padx=5,pady=5, fill=tk.X, expand=True)

        #find serial ports
        self.findSerialPorts()
        tk.Button(self.deviceSelFrame, text='Test Connection', command=self.testConnection).pack(side=tk.LEFT, padx=5, pady=5)

        #Jog Controls
        self.jogControlFrame=ttk.LabelFrame(self.controlFrame, text='Jog Controls')
        self.jogControlFrame.pack(pady=5, expand=True, fill=tk.X)
        self.jogFrame=tk.Frame(self.jogControlFrame)
        self.jogFrame.pack()
        tk.Button(self.jogFrame, text='Y+').grid(row=0, column=1, rowspan=2, sticky=tk.NSEW)
        tk.Button(self.jogFrame, text='X-').grid(row=2, column=0, rowspan=2, sticky=tk.NSEW)
        tk.Button(self.jogFrame, text='X+').grid(row=2, column=2, rowspan=2, sticky=tk.NSEW)
        tk.Button(self.jogFrame, text='Y-').grid(row=4, column=1, rowspan=2, sticky=tk.NSEW)
        tk.Label(self.jogFrame, text='      ').grid(row=0, column=3,rowspan=2)
        tk.Button(self.jogFrame, text='Z+').grid(row=1, column=4, rowspan=2,sticky=tk.NSEW)
        tk.Button(self.jogFrame, text='Z-').grid(row=3, column=4, rowspan=2,sticky=tk.NSEW)

        self.jogRateFrame=tk.Frame(self.jogControlFrame)
        self.jogRateFrame.pack()

        tk.Label(self.jogRateFrame, text='Jog Rate:').pack(side=tk.LEFT, padx=5, pady=5)
        tk.Entry(self.jogRateFrame).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.jogRateFrame, text='x10').pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.jogRateFrame, text='/10').pack(side=tk.LEFT, padx=5, pady=5)

        #Home Controls
        self.homeControlFrame=ttk.LabelFrame(self.controlFrame, text='Home Controls')
        self.homeControlFrame.pack(expand=True, fill=tk.X)
        tk.Button(self.homeControlFrame, text='Home X').pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(self.homeControlFrame, text='Home Y').pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(self.homeControlFrame, text='Home Z').pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(self.homeControlFrame, text='Auto Home').pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(self.homeControlFrame, text='Go Home').pack(side=tk.LEFT, padx=2, pady=5)

        #Gcode Control
        self.gcodeControlFrame=ttk.LabelFrame(self.controlFrame, text='Gcode')
        self.gcodeControlFrame.pack(fill=tk.BOTH, expand=True)
        self.gcodeFrame=tk.Frame(self.gcodeControlFrame)
        self.gcodeDisplay=tk.Text(self.gcodeFrame,height=10,width=50,background='white')
        
        # put a scroll bar in the frame
        self.gcodeScroll=tk.Scrollbar(self.gcodeFrame)
        self.gcodeDisplay.configure(yscrollcommand=self.gcodeScroll.set)

        self.gcodeDisplay.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.gcodeScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.gcodeFrame.pack(fill=tk.BOTH, expand=True)
        
        
        #create a frame to show machine graphics
        self.graphics=tk.Frame(parent,relief=tk.RAISED, bd=2)
        self.graphics.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        tk.Label(self.graphics).pack(expand=True, fill=tk.BOTH)

    def pause(self):
        if self.pauseButtontext.get()=='Pause':
            self.pauseButtontext.set('Resume')
            self.pauseButton['bg']='yellow'
        elif self.pauseButtontext.get()=='Resume':
            self.pauseButtontext.set('Pause')
            self.pauseButton['bg']='green'

    def status(self):
        if self.statusButtontext.get()=='Enable':
            self.connect()
            self.statusButtontext.set('Disable')
            self.enableButton['bg']='green'
        elif self.statusButtontext.get()=='Disable':
            self.closeConnection()
            self.statusButtontext.set('Enable')
            self.enableButton['bg']='red'

    def findSerialPorts(self):
        temp=glob.glob('/dev/serial/by-id/*')+glob.glob('/dev/tty*')
        
        self.grblDeviceCombo['values']=temp

    def testConnection(self):
        try:
            self.serialCon = serial.Serial(self.grblDevice.get(),9600,timeout =1)
        except:
            box.showerror('Error','Could Not Open Port')
            return
        
        self.wakeUp()
        self.serialCon.write('G92 x0 y0 z0' + '\n') # Send g-code block to grbl
        grbl_out = self.serialCon.readline() # Wait for grbl response with carriage return
        if grbl_out.strip()=='ok':
            box.showinfo('Good Connection','Good Connection')
        else:
            box.showerror('Error','Connection timed out')
        self.serialCon.close()

    def eStop(self):
        pass

    def connect(self): 
        # Open grbl serial port
        self.serialCon = serial.Serial(self.grblDevice.get(),9600)

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

    def closeConnection(self):
        self.serialCon.close()

if __name__ == '__main__':
    root = tk.Tk()
    app=gui(root)
    root.mainloop()
