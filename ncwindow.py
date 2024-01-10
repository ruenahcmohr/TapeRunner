#from tkinter import * 
#import tkFileDialog

from tkinter import filedialog
from tkinter import *


class NC_file(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent.parent)   
        self.parent = parent    
        
        self.Line = 1  
        self.jump_enable = True          

        fileMenu = Menu(parent.menubar, tearoff=0)
        fileMenu.add_command(label="Open", command = self.open_command)
        fileMenu.add_command(label="Save As", command = self.save_command)        
        self.parent.menubar.add_cascade(label="File", menu=fileMenu)        

        self.filename = StringVar( self ) 
        self.filename.set("-")
        self.fname = Label(self, textvariable = self.filename);
        self.fname.pack()

        self.txt = Text(self, width=5, height=1)
        self.txt.pack(side = LEFT, fill=BOTH, expand=1)    
            
        self.txt.insert(END, "NC FILE GOES HERE.\n")
        self.txt.tag_configure("current_line", foreground="#FFFFFF", background="#0000ee")
        self.txt.tag_add('current_line', str(self.Line)+'.0', str(self.Line+1)+'.0')
        self.txt.bind("<ButtonRelease-1>", self.jump_line)

        self.scroll = Scrollbar(self, command=self.txt.yview, width=10)
        self.txt['yscrollcommand'] = self.scroll.set
        self.scroll.pack(side = LEFT, fill=Y)
        
    def open_command(self):
      if (self.jump_enable):
        ftypes = [('NC files', '*.nc'), ('All files', '*')]
        
        filename = filedialog.askopenfilename(filetypes=ftypes)
        if filename:
         # yea we need sanity checks added in here      
            iofile = open(filename, "r")
            self.filename.set(filename)
            self.txt.delete(1.0, END)
            self.txt.insert(END, iofile.read())
            iofile.close()
            self.set_line_num(1)            

    def save_command(self):
        ftypes = [('NC files', '*.nc'), ('All files', '*')]
        iofile = filedialog.asksaveasfile(mode='w', filetypes = ftypes)
        if iofile != None:
             self.filename.set(iofile.name)
             data = self.txt.get('1.0', END+'-1c')
             iofile.write(data)
             iofile.close()
             
             
    def set_line_num(self, N):
        self.Line = N
        self.txt.tag_remove('current_line', 1.0, "end")
        self.txt.tag_add('current_line', str(self.Line)+'.0', str(self.Line+1)+'.0')
        self.txt.see(str(N)+'.0')
        
    def jump_line(self, event):
       if (self.jump_enable):
         if (self.parent.machine.Execute != 1):
           self.set_line_num(int(self.txt.index('insert').split('.')[0]))
    
    def get_line(self):   
       s = self.txt.get( str(self.Line)+'.0', str(self.Line+1)+'.0').strip()+"\r\n"
       s = s.encode('ascii','ignore')
       l = int(self.txt.index('end').split('.')[0])       
       self.Line += 1        
       if (self.Line > l):
         return NONE
       else:
         self.txt.see(str(self.Line+8)+'.0')
         self.set_line_num(self.Line)
         return s.decode()
         
    def spooltest(self):
      s = self.get_line()
      while (s):
         print (s.strip())
         s = self.get_line()
   
