
import threading
from tkinter import *
import time 

class Stopwatch(Label):

    def __init__(self, *args, **kwargs):
     Label.__init__(self, *args, **kwargs)
     self.timerText = StringVar( self ) 
         
     self.timerText.set("Elapsed: 0:0:0")
     self.config(textvariable = self.timerText)
     self.startTime = time.time()
     self.running   = False
     self.cycle     = True
     self.update()
    
    # FOR FOX SAKE, python cant clean up threads properly.
    #    and there is no way to interrupt the running timer.
    def terminate(self):
      print ("Please allow me 1 second while I figure out how to quit.")
      self.cycle = False
    
    def start(self):
      self.running = True
        
    def stop(self):
      self.running = False
        
    def reset(self):
      self.startTime  = time.time()

    def update(self):
      if (self.cycle):
       if (self.running):
         totTime = time.time() - self.startTime
         hours   = int(totTime / 3600)
         totTime -= hours * 3600
         minutes = int(totTime / 60)
         totTime -= minutes * 60
         seconds = int(totTime)
         self.timerText.set ('Elapsed: '+str(hours).zfill(2)  + ':' + str(minutes).zfill(2)  + ':' + str(seconds).zfill(2) )              
       self.timer = threading.Timer(1.0, self.update).start()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
