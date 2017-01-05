# Sorry I'm not a long-standing python programmer, 
# I'm making this up as I go.
# coding techniques employed:  pseudorandom-spiderweb, s (otherwise 'Stupidly short variable names'), 
#                                global-fixedit!, CammelCase, anti-oops, oneWindow-functions.

from Tkinter import *
import tkFileDialog
import threading
import serial
from tkdialog import GetComm
import tkMessageBox
import time
# damn, the replies from grbl are evil.
import re


NCLine     = 1
Execute    = 0
CommName   = ""
BaudRate   = 0
CommPort   = serial.Serial(timeout=0)
startTime  = time.time()

# FOR FOX SAKE, readline will return what its got if it can't find a newline,
# which means, we have to buffer the data we have to poll because its got no callback.
# AND nobody has a proper method to print time!?! 
SerialBuff = ""


def updateElapsedTime():
  global startTime
  global timerText
  global Execute
  if (Execute != 0):
   totTime = time.time() - startTime
   hours = int(totTime / 3600)
   totTime -= hours * 3600
   minutes = int(totTime / 60)
   totTime -= minutes * 60
   seconds = int(totTime)
   timerText.set ('Elapsed: '+str(hours).zfill(2)  + ':' + str(minutes).zfill(2)  + ':' + str(seconds).zfill(2) )
  threading.Timer(1.0, updateElapsedTime).start()

def sendstring():
    if (CommPort.isOpen() ):
      history.insert(END, e.get()+'     ')
      limitHistory()
      CommPort.write(e.get()+'\n')
    else:
     CommAlertUnopen()
     
     
def loadNCfile():
    fname = tkFileDialog.askopenfilename(filetypes=(("NC files", "*.nc"),("All files", "*.*") ))
    if fname:
       try:
          with open(fname) as f:
	    filenameText.set(fname)
            NCfile.delete(1.0, END)
            NCfile.insert(END, f.read())
            f.close()
            
       except:                     # <- naked except is a bad idea
          showerror("Open Source File", "Something went wrong, I don't know what.\n'%s'" % fname)
       return

def limitHistory():
  count = int(history.index('end-1c').split('.')[0])
  if (count > 14):
    history.delete(1.0, 2.0)

def startSend():
  global Execute
  global startTime
  if (CommPort.isOpen() ):
    if Execute == 0:
      startTime  = time.time()
      Execute = 1
      sendLine()
    Execute = 1
  else: 
    CommAlertUnopen()

def pauseSend():
  global Execute
  Execute = 0.5
  
def stopSend():
  global Execute
  global NCLine
  NCfile.tag_remove('current_line', 1.0, "end")
  NCLine = 1
  Execute = 0

def sendLine():
  global NCLine
  global Execute
  if Execute != 0:
    if Execute == 1:
      tapeStep()
 #   threading.Timer(2.0, sendLine).start()

def tapeStep():
   global NCLine
   global Execute
   if (CommPort.isOpen() ):
#     NCfile.see(str(NCLine+8)+'.0')
#     NCfile.tag_remove('current_line', 1.0, "end")
#     NCfile.tag_add('current_line', str(NCLine)+'.0', str(NCLine+1)+'.0')
     s = NCfile.get( str(NCLine)+'.0', str(NCLine+1)+'.0').strip()+"\r\n"
     c = s.strip()
     CommPort.write(c + '\n')
     history.insert(END, c + '      ')
     limitHistory()
     NCLine += 1 
     NCfile.see(str(NCLine+8)+'.0')
     NCfile.tag_remove('current_line', 1.0, "end")
     NCfile.tag_add('current_line', str(NCLine)+'.0', str(NCLine+1)+'.0')
     if (NCLine > int(NCfile.index('end-1c').split('.')[0])): 
        Execute = 0
        NCLine = 1
        print "Run Finished."
        NCfile.tag_remove('current_line', 1.0, "end")       
   else:
     CommAlertUnopen()


def donothing():
   filewin = Toplevel(mainwin)
   button = Button(filewin, text="Do nothing button")
   button.pack()
   
def CommAlertUnopen():
   tkMessageBox.showwarning("Ninny",  "The YOUthere will first open a serial port by clicking Communication -> Connect." )   

def CommAlertSettings():
  tkMessageBox.showwarning("Ninny",  "The YOUthere will first select a device to use by clicking Communication -> Setup." )   

def serialSetup():
   commport = GetComm(mainwin)
   mainwin.wait_window(commport.serDialogWin)
   if (commport.success ):     
     print commport.portResult
     print commport.baudResult
     #CommName = commport.portResult
     #BaudRate = commport.baudResult
     CommPort.baudrate = commport.baudResult
     CommPort.port = commport.portResult


def serialOpen():
   CommPort.open()
   print CommPort.fd
    

def serialClose():
   global SerialBuff
   CommPort.close()
   SerialBuff = ''

def jumpToLine(event):
  global NCLine
  global Execute
  # dont jump if were running. 
  # if paused ok
  if (Execute != 1):
    NCfile.tag_remove('current_line', 1.0, "end")
    NCfile.tag_add('current_line', "insert linestart", "insert lineend")
    NCLine = int(NCfile.index('insert').split('.')[0])


#you cannot get an event for recieved characters in python serial
#so this has to be polled :(
def serialService():
  global SerialBuff  
  mainwin.after(41, serialService)
  if (CommPort.isOpen() ):
    if ( CommPort.inWaiting() > 0 ):                           # if we have data....
      SerialBuff += CommPort.read(CommPort.inWaiting())        # read data, append to buffer, no, readline will (now) just do the same thing.
      
#    if (SerialBuff[0] == '\r'): 
#      if (len(SerialBuff) == 1): SerialBuff = ""
#      else :                     SerialBuff = SerialBuff[1:]  # aparently we need to dispose of leading returns ourselfs      
      #    if (SerialBuff[0] == '\n'): SerialBuff = SerialBuff[1:]

    SerialBuff = SerialBuff.lstrip("\n\r")
#   SerialBuff = SerialBuff.strip("\n")                     # remove newlines, grbl gives us both            
    if (len(SerialBuff) > 0):       
      print str(len(SerialBuff))
#      for ch in SerialBuff:
#        print ch.encode('hex')+" ",
#      print "\n"
      if (len(SerialBuff.split("\r")) > 1):                    # do we have a whole line yet?
        thisLine = SerialBuff.split("\r")[0]                   # if so, get one...
#	updateElapsedTime()
        SerialBuff = SerialBuff[len(thisLine):]                # trim off what we just got
        print thisLine  
	history.insert(END, thisLine + '\n')
        limitHistory()   
	# *** exception!!! if this is a reply from a status request, do NOT gate a new nc command!
        if      ( thisLine == "ok" ):  
          sendLine()       #print "WE GOT OK!"                        # clear handshake flag
        elif ( thisLine[:6] == "error:"): 
          print "OOPS, It didn't like that, trying to ignore, lalala..."   # WHY ARE YOU ASKING ME WHAT TO DO????
          sendLine()                             #maybe it'll forgive us and we can move on?
        elif ( thisLine[:1] == "<"): 
          print "Status update..."
          # oh, parsing this will be a MESS
          # < AAAAAA, BBB, CCC, DDD, EEE, ... >  where if *POS, next 3 params are position.
	  #  if AAAAAA will be status: _Pos####, ...
          thisLine = thisLine.strip("<>")  # remove the brackets...
	  # now we have:  'status: 
	  rply = re.search('^(.+):', thisLine)
	  print rply.group(0)
	  
	  
	  

def unused1() :	  
          for s in (thisLine.split(",")):  # nono, they used a : for the first one and , for the rest, ARG
            if (s == "WPos:" ):
	      pflag = 1
	      print "Work Position:",
	    else: 
	      pflag = 0
	    if (pflag > 0):
	      print s + " ",
	      pflag += 1
	      if (pflag == 4): pflag = 0
	    else: 
	      print s


mainwin = Tk()
mainwin.title("TapeRunner")
mainwin.wm_iconbitmap('@icon.xbm') 

timerText  = StringVar(mainwin)
filenameText = StringVar(mainwin)

menubar = Menu(mainwin)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", underline=0, command=loadNCfile)
filemenu.add_separator()
filemenu.add_command(label="Quit", underline=0, command=mainwin.quit)
menubar.add_cascade(label="File",  underline=0, menu=filemenu)

runmenu = Menu(menubar, tearoff=1)
runmenu.add_command(label="Step",    underline=0, command=tapeStep)
runmenu.add_command(label="Run",     underline=0, command=startSend)
runmenu.add_command(label="Pause",   underline=0, command=pauseSend)
runmenu.add_command(label="Stop",    underline=0, command=stopSend)

menubar.add_cascade(label="Program", underline=0, menu=runmenu)

commmenu = Menu(menubar, tearoff=0)
commmenu.add_command(label="Setup",        underline=0, command=serialSetup)
commmenu.add_command(label="Connect",      underline=0, command=serialOpen)
commmenu.add_command(label="Disconnect",   underline=0, command=serialClose)
menubar.add_cascade(label="Communication", underline=0, menu=commmenu)

pendantmenu = Menu(menubar, tearoff=0)
pendantmenu.add_command(label="Setup",        underline=0, command=donothing)
pendantmenu.add_command(label="Connect",      underline=0, command=donothing)
pendantmenu.add_command(label="Disconnect",   underline=0, command=donothing)
menubar.add_cascade(label="peNdant", underline=0, menu=pendantmenu)

mainwin.config(menu=menubar)

fo = Button(mainwin, text="Open", width=4, command=loadNCfile)
fo.grid(row=0, column=0, sticky=W)

stat = Label(mainwin, textvariable=timerText)
stat.grid(row=0, column=2, sticky=W)
timerText.set("0:0:0")

lastFile = Label(mainwin, textvariable=filenameText)
lastFile.grid(row=0, column=1, sticky=W)
filenameText.set("")

NCfile = Text(mainwin, width=50, height=15, wrap=NONE, background="#eeeeee")
NCfile.grid(row=1,column=0, rowspan=2, columnspan=2, sticky=N+E+S+W)
NCfile.insert(END, "NC FILE GOES HERE.\n")
NCfile.tag_configure("current_line", foreground="#FFFFFF", background="#0000ee")
NCfile.tag_add('current_line', str(NCLine)+'.0', str(NCLine+1)+'.0')
NCfile.bind("<ButtonRelease-1>", jumpToLine)

NCscroll = Scrollbar(mainwin, command=NCfile.yview, width=10)
NCfile['yscrollcommand'] = NCscroll.set
NCscroll.grid(row=1,column=1, rowspan=2, sticky=N+E+S)

history = Text(mainwin, width=50, height=15, foreground="#10FF10", background="#020202" )
history.grid(row=1,column=2, columnspan=2, sticky=N+E+S+W)
history.insert(END, "   -- MACHINE HISTORY. --\n")
history.bind("<Key>", lambda e: "break")

e = Entry(mainwin)
e.grid(row=2,column=2, sticky=E+W)
e.bind("<Return>",(lambda event: sendstring()))
e.focus_set()

b = Button(mainwin, text="Send", width=4, command=sendstring).grid(row=2, column=3)

mainwin.after(10, serialService)
#thread = threading.Thread(target=recieverLoop, args=())
#once a thread is started in python you cannot force stop it
#thread.start()
updateElapsedTime()

mainloop()



