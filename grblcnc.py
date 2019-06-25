
from Tkinter import * 
from historyWindow import *
from stopwatch import *
from selectcomm import *
import serial
import re


class grbl_cnc(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.parent)   
        self.parent = parent    
        
        self.SerialBuff = ""
        
        self.stopwatch = Stopwatch(self)
        self.stopwatch.pack(fill=X)
        
        self.History = HistoryWindow(self)
        self.History.pack(fill=BOTH, expand=1)
                  
        self.entry = Entry(self)
        self.entry.pack(side = LEFT, fill=X, expand=1)    
        self.entry.bind("<Return>",(lambda event: self.send_command()))   
       
         
        self.enterbutton = Button(self, text="Send", width=4, command=self.send_command)
        self.enterbutton.pack(side=LEFT)
         
        self.CNCMenu = Menu(parent.menubar, tearoff=1)
        self.CNCMenu.add_command(label="Step",       command = self.step_command, state='disabled')
        self.CNCMenu.add_command(label="Run",        command = self.run_command, state='disabled')
        self.CNCMenu.add_command(label="Pause",      command = self.pause_command, state='disabled')
        self.CNCMenu.add_command(label="Stop",       command = self.stop_command, state='disabled')   
        self.CNCMenu.add_separator()   
        self.CNCMenu.add_command(label="Connect",    command = self.connect_command, state='disabled')
        self.CNCMenu.add_command(label="Disconnect", command = self.disconnect_command, state='disabled')
        self.CNCMenu.add_command(label="Setup",      command = self.setup_command)        
        self.parent.menubar.add_cascade(label="Machine", menu=self.CNCMenu )                               
        
        self.CommPort  = serial.Serial(timeout=0)
        self.Execute   = 0
        self.WaitAck   = False       
        
        self.after(10, self.serialService)
       # fileMenu.entryconfigure('Step', state = 'disabled')

    def terminate(self):
      self.stopwatch.terminate()
  
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
        self.CNCMenu.entryconfigure('Step',  state = 'normal')
        self.CNCMenu.entryconfigure('Run',   state = 'normal')   
        self.CNCMenu.entryconfigure('Pause', state = 'normal')
        self.CNCMenu.entryconfigure('Stop',  state = 'normal')     
      return
      
    def disconnect_command(self):
      if (self.CommPort.isOpen()):
        self.CommPort.close()
        self.CNCMenu.entryconfigure('Step',  state = 'disabled')
        self.CNCMenu.entryconfigure('Run',   state = 'disabled')   
        self.CNCMenu.entryconfigure('Pause', state = 'disabled')
        self.CNCMenu.entryconfigure('Stop',  state = 'disabled')  
      return
     
        
    def step_command(self):      
      self.sendLine()     
     
    def run_command(self):
        if self.Execute == 0:          
          self.stopwatch.reset()          
          self.sendLine()
        self.Execute = 1
        self.stopwatch.start()
        
    def pause_command(self):
        self.Execute = 0.5
        self.stopwatch.stop()
    
    def stop_command(self):
      self.parent.ncfile.set_line_num(1)
      self.Execute = 0
      self.stopwatch.stop()
    
    def send_command(self):
      self.sendString(self.entry.get())                  

# this gets rather intersting, we dont want to know if we just got an ok,
# we want to generalize this as 'did we just get a reply at all'
# knowing if its an OK or if its an error is secondary
# if one line has multiple G commands on it, we get multiple OK's ?

    def serialService(self):
      self.after(41, self.serialService)
      if (self.CommPort.isOpen() ):
        if ( self.CommPort.inWaiting() > 0 ):                           # if we have data....
           self.SerialBuff += self.CommPort.read(self.CommPort.inWaiting())        # read data, append to buffer, no, readline will (now) just do the same thing.                      
        self.SerialBuff = self.SerialBuff.lstrip("\n\r")                   # remove wayward cr/lf  
        if (len(self.SerialBuff) > 0):                         #do we have data?
         r = re.match(r"(.*?[\r|\n]+)", self.SerialBuff)       # do we have a line?
         if r is not None:
           thisLine = r.group(0)                                #capture whole line
           self.SerialBuff = self.SerialBuff[len(thisLine):]                # trim off what we just got           
           thisLine = thisLine.strip("\r\n")
	   self.History.appendLine("   "+thisLine + "\n")
           self.processLine(thisLine)        
        
         
    def processLine(self, thisLine):
            if ( thisLine == "ok" ):  
               self.reply_ok()
            elif ( thisLine[:6] == "error:"): 
               self.reply_error(thisLine)
            elif ( thisLine[:1] == "<"): 
               self.reply_status(thisLine)
 
    def reply_ok(self):
      # WaitAck should be true, if its not, wtf just got an OK?
      if (self.Execute == 1):  # get a line and send it.
        self.sendLine()  # this needs to be a flag so that, when resuming from a pause, we know if we can send a line right away.
       
    def reply_error(self, details):
      #Eddy lost a g-string, and he tried to keep going, but it sounded like hell.
      if (self.Execute == 1):  # get a line and send it.
        self.sendLine() 
      
    def reply_status(self, details):
#              # oh, parsing this will be a MESS
#              # < AAAAAA, BBB, CCC, DDD, EEE, ... >  where if *POS, next 3 params are position.
#	      #  if AAAAAA will be status: _Pos####, ...
#              thisLine = thisLine.strip("<>")  # remove the brackets...
#	      # now we have:  'status: 
#	      rply = re.search('^(.+):', thisLine)
#	      print rply.group(0)
      return
             
             
    def sendLine(self):
        s = self.parent.ncfile.get_line()
        if (s != NONE):
           c = s.strip("\r\n")
           self.WaitAck = True
           self.sendString(c)
        else:
           self.Execute = 0
           self.stopwatch.stop()
           self.parent.ncfile.set_line_num(1)
	   c = self.stopwatch.timerText.get()
           print "Run Finished. " + c
        return                     
             
             
    def sendString(self, string):      
        if (self.CommPort.isOpen() ):
          self.History.appendLine(string + "     ")
          self.CommPort.write(string.encode() + "\n")           #\r or \n, but not both!

    
    
    
    
    
    
     
