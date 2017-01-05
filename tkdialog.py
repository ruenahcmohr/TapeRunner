from Tkinter import *
import serial
# this is python-serial v2.6-1 + (debian)
#  oh, and its broken, so you have to apply "fix #26"
#
#Index: trunk/pyserial/serial/tools/list_ports_posix.py
#===================================================================
#--- trunk/pyserial/serial/tools/list_ports_posix.py (revision 439)
#+++ trunk/pyserial/serial/tools/list_ports_posix.py (working copy)
#@@ -64,7 +64,8 @@
#                 )
#
#     def usb_lsusb_string(sysfs_path):
#-        bus, dev = os.path.basename(os.path.realpath(sysfs_path)).split('-')
#+        base = os.path.basename(os.path.realpath(sysfs_path))
#+        bus, dev = base.split('-')
#         try:
#             desc = popen(['lsusb', '-v', '-s', '%s:%s' % (bus, dev)])
#             # descriptions from device
#
#
import serial.tools.list_ports
import ttk
 

class GetComm(): 

  def cancel(self):
    self.baudResult = 0 
    self.portResult = "" 
    self.serDialogWin.destroy()
    self.success = False
    
  def doOpen(self):
    self.baudResult = self.baud.get() 
    self.portResult = self.ports.get() 
    self.serDialogWin.destroy()
    self.success = True


  def __init__(self, parent):  

    #self.serDialogWin = Tk()
    self.serDialogWin = Toplevel(parent)
    self.serDialogWin.title("Open Port")

    self.portLabel = Label(self.serDialogWin, text="PORT").grid(column = 0, row=0, padx=5, pady=5)

    self.portName = StringVar()
    self.ports = ttk.Combobox(self.serDialogWin, textvariable=self.portName)

    self.portList = []
    for n, (self.portname, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports())):
     self.portList.append(self.portname)
    self.ports['values'] = tuple(self.portList)

    self.ports.current(0)
    self.ports.grid(column=1, row=0, padx=5, pady=5)

    self.baudLabel = Label(self.serDialogWin, text="BAUD").grid(column = 0, row=1, padx=5, pady=5)

    self.baudRate = StringVar()
    self.baud = ttk.Combobox(self.serDialogWin, textvariable=self.baudRate)

    self.baudList = []
    for n, baudrate in enumerate(serial.Serial.BAUDRATES):
      if (baudrate > 149):
        self.baudList.append(str(baudrate))
    self.baud['values'] = tuple(self.baudList)

    self.baud.current(8) # 12 is 115200
    self.baud.grid(column=1, row=1, padx=5, pady=5)


    self.btnOpen = Button(self.serDialogWin, text="Yup", width=4, command=self.doOpen)
    self.btnOpen.grid(row=2, column=1, sticky=E, padx=5, pady=5)

    self.btnCancel = Button(self.serDialogWin, text="Cancel", width=4, command=self.cancel)
    self.btnCancel.grid(row=2, column=0, sticky=E, padx=5, pady=5)

    #self.serDialogWin.mainloop()


#foo = GetComm()
#print foo.success
#print foo.portResult
#print foo.baudResult

