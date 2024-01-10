from tkinter import * 
from selectcomm import *
import serial


class rue_pendant():

    def __init__(self, parent):
        self.parent = parent    
        
        self.SerialBuff = ""
        self.mode = 0;
                 
        self.CNCMenu = Menu(parent.menubar, tearoff=1)
        self.CNCMenu.add_command(label="Connect",    command = self.connect_command, state='disabled')
        self.CNCMenu.add_command(label="Disconnect", command = self.disconnect_command, state='disabled')
        self.CNCMenu.add_command(label="Setup",      command = self.setup_command)        
        self.parent.menubar.add_cascade(label="Pendant", menu=self.CNCMenu )                               
        
        self.CommPort  = serial.Serial(timeout=0)
        self.Execute   = 0
        self.WaitAck   = False       
        
       # self.parent.after(10, self.serialService)
       # fileMenu.entryconfigure('Step', state = 'disabled')

    def setup_command(self):
      commport = SelectComm(self)
      self.wait_window(commport.serDialogWin)
      if (commport.success ):     
        self.CommPort.baudrate = commport.baudResult
        self.CommPort.port     = commport.portResult
        self.CNCMenu.entryconfigure('Connect', state = 'normal')
        self.CNCMenu.entryconfigure('Disconnect', state = 'normal')
      return
      
    def connect_command(self):
      if (self.CommPort.port != ""):
        self.SerialBuff = ""
        self.Handshake = 0
        self.CommPort.open()   
        # gee, this is a lot of code...   
      return
      
    def disconnect_command(self):
      if (self.CommPort.isOpen()):
        self.CommPort.close()        
      return
      
    def serialService(self):
    #  self.parent.after(41, self.serialService)
      if (self.CommPort.isOpen() ):
        if ( self.CommPort.inWaiting() > 0 ):                           # if we have data....
          self.SerialBuff += self.CommPort.read(self.CommPort.inWaiting())        # read data, append to buffer, no, readline will (now) just do the same thing.      
        self.SerialBuff = self.SerialBuff.lstrip("\n\r")                   # remove newlines, grbl gives us both            
        if (len(self.SerialBuff) > 0):       
           return
           
           
   


