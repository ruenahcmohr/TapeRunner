# Sorry I'm not a long-standing python programmer, 
# I'm making this up as I go.
# coding techniques employed:  pseudorandom-spiderweb, s (otherwise 'Stupidly short variable names'), 
#                                global-fixedit!, CammelCase, anti-oops, oneWindow-functions.

from Tkinter import *



class HistoryWindow(Text):
  
   def __init__(self, *args, **kwargs):
     Text.__init__(self, *args, **kwargs)
     self.bind("<Key>", lambda e: "break")
     self.config(self, width=5, height=2)
     self.config(foreground="#10FF10", background="#020202")
     
   def appendLine(self, string ):
        self.insert(END, string)
	self.see(END)
        self.limitHistory()
   
   def limitHistory(self):
     count = int(self.index('end-1c').split('.')[0])
     #if (count > 15):
     if (count > 100):
       self.delete(1.0, 2.0)


   
   
   
