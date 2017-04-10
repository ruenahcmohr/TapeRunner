
from Tkinter import * 
from grblcnc import *
from tkMessageBox import *
from ncwindow import *
from pendant import *

class MyApp():

  def __init__(self, parent):
    self.parent = parent
    parent.geometry("600x250+300+300")
    parent.title("Tape Runner II")

    self.menubar = Menu(parent)
    parent.config(menu=self.menubar)
    
    appMenu = Menu(self.menubar, tearoff=0)
    appMenu.add_command(label="Exit", command = self.packup)
    self.menubar.add_cascade(label="App", menu=appMenu)  
        
    self.layout = PanedWindow()
    self.layout.pack(fill=BOTH, expand=1)
      
    self.ncfile = NC_file(self)
    self.layout.add(self.ncfile, width=300)

    self.machine = grbl_cnc(self)
    self.layout.add(self.machine)   
    
    self.pendant = rue_pendant(self)                     
    
    # The world has forgotten about right justified help menus and we cant do them anymore.
    aboutMenu = Menu(self.menubar, tearoff=0)
    aboutMenu.add_command(label="About", command = self.about)
    self.menubar.add_cascade(label="Help", menu=aboutMenu)  

  def packup(self):
    self.parent.withdraw()
    self.machine.terminate()
    self.parent.quit()    

  def about(self):
    showinfo(message='NC File spooler for GRBL \ncompliments of Rue Mohr')

root = Tk()
root.wm_iconbitmap('@icon.xbm')
app = MyApp(root)
root.protocol("WM_DELETE_WINDOW", app.packup)
root.mainloop()
