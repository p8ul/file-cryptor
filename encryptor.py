try:
    from Tkinter import *
    import Tkinter
except:
    from tkinter import *
import Tkconstants, tkFileDialog
import Pmw
import time
#from pygsm import GsmModem
#import pygsm
import csv
import os
import shutil
from os import path

import demo    


root = Tkinter.Tk()
root.title("File Security")
#root.geometry('2000x700+150+150')

class App:
    def __init__(self, parent):
        #windows size        
        self.dialog = Pmw.CounterDialog(parent,
                                        label_text = 'conn',
                                        counter_labelpos = 'n',
                                        entryfield_value = 'con1',
                                        buttons = ('OK', 'Cancel'),
                                        defaultbutton = 'OK',
                                        title = 'set post',
                                        command = self.execute)
        self.dialog.withdraw()
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'
        self.filename = ''

        #Tkinter.Button(parent, text='askopenfilename', command=self.askopenfilename).pack(**button_opt)
        # Create button to launch the dialog.
        #w = Tkinter.Button(parent,bg="white",text = "Select File", command = self.askopenplanfile)
        #w.pack(padx = 8, pady = 8)
        w11 = Pmw.Group(parent,hull_bg='#F2F3F4',tag_bg='#F2F3F4',
              tag_fg='red',ring_bg='#F2F3F4',
              tag_text='File Security ',tagindent=150)
        w11.pack(fill=BOTH, expand=1, padx=6, pady=6)
        nb = Pmw.NoteBook(parent)
        p1 = nb.add('Encryption')
        p2 = nb.add('Decryption')
        
        nb.pack(padx=5, pady=5, fill=BOTH, expand=1)
        g1 = Pmw.Group(p1, tag_text='Encryption')
        g1.pack(fill=BOTH, side=LEFT, padx=6, pady=6)

        g2 = Pmw.Group(p2, tag_text='Decryption')
        g2.pack(fill=BOTH, side=RIGHT, padx=6, pady=6)

        #*********************************************************************** 
        #page one (encryption)  ------------ file encryption--------------
        #***********************************************************************
        self.password = Pmw.EntryField(g1.interior(), labelpos=W, label_text='Password',entry_show='-',validate = None)
        self.output = Pmw.EntryField(g1.interior(), labelpos=W, label_text='Output FileName',validate = None)
        self.plainfile = Pmw.EntryField(g1.interior(), labelpos=W, label_text = 'File):',validate = None,entry_state=DISABLED, value = 'file to encrypt')
        
        widgets = (self.password, self.output,self.plainfile)
        for widget in widgets:
            widget.pack(fill=X, expand=1, padx=10, pady=5)
        Pmw.alignlabels(widgets)
        self.password.component('entry').focus_set()
        
        #*****************************
        #encryption action buttons
        #*****************************
        
        buttonBox = Pmw.ButtonBox(g1.interior(), labelpos='nw', label_text='Browse Plaintext:')
        buttonBox.pack(fill=BOTH, expand=1, padx=10, pady=10)
        buttonBox.add('Browse..', command = lambda b='apply': self.askopenplanfile(b))
        buttonBox.add('Encrypt', command = lambda b='ok': self.Encrypt(b))        
        buttonBox.add('Exit', command = lambda b='cancel': self.buttonPress(b))
        buttonBox.setdefault('Encrypt')
       

        #***************************************************************
        #page two (decryption) ------------ decryption --------------
        #***************************************************************
        self.dpassword = Pmw.EntryField(g2.interior(), labelpos=W, label_text='Password',entry_show='-',validate = None)
        self.doutput = Pmw.EntryField(g2.interior(), labelpos=W, label_text='Output FileName',validate = None)
        self.encryptedfile = Pmw.EntryField(g2.interior(), labelpos=W, label_text = 'File):',validate = None,entry_state=DISABLED, value = 'file to encrypt')
        
        widgets = (self.dpassword, self.doutput,self.encryptedfile)
        for widget in widgets:
            widget.pack(fill=X, expand=1, padx=10, pady=5)
        Pmw.alignlabels(widgets)
        self.password.component('entry').focus_set()        
        
        #*****************************
        #decryption action buttons
        #*****************************
        buttonBox = Pmw.ButtonBox(g2.interior(), labelpos='nw', label_text='Browse encrypted file:')
        buttonBox.add('Browse..', command = lambda b='apply': self.askopenencryptedfile(b))
        buttonBox.pack(fill=BOTH, expand=1, padx=10, pady=10)
        buttonBox.add('Decrypt', command = lambda b='ok': self.Decrypt(b))
        #buttonBox.add('Decrypt', command = lambda b='apply': self.Decrypt(b))
        buttonBox.add('Exit', command = lambda b='cancel': self.buttonPress(b))
        buttonBox.setdefault('Decrypt')
        
        self.st = Pmw.ScrolledText(parent, borderframe=1, labelpos=N,
                    label_text='File Preview', usehullsize=1,
                    hull_width=400, hull_height=300,
                    hull_bg='#F2F3F4',label_bg='#F2F3F4',label_fg='#007FFF',
                    text_padx=10, text_pady=10,text_bg='white',text_fg='black',
                    borderframe_bg='#9966CC',vertscrollbar_bg='#FF7E00',
                    text_wrap='none')
        try:
            self.st.importfile('data.txt')
        except:
            dt = open('data.txt','a+')
            self.st.importfile('data.txt')
            dt.close()
        self.st.pack(fill=BOTH, expand=1, padx=5, pady=5)
        #end scrolltext

	
    def askopenplanfile(self,result):   
        self.filename = tkFileDialog.askopenfilename(**self.file_opt)
        print(self.filename)
        self.plainfile.setentry(self.filename)
        self.st.clear()
        self.st.importfile(self.filename)
        
    def askopenencryptedfile(self,result):   
        self.filename2 = tkFileDialog.askopenfilename(**self.file_opt)
        print('file: '+self.filename2+'')
        self.encryptedfile.setentry(self.filename2)
        self.st.clear()
        self.st.importfile(self.filename2)
        
    def Encrypt(self,result):
        print 'Encrypting file'
        password = self.password.getvalue()
        output = self.output.getvalue()
        print 'password: '+str(password)+' length: '+str(len(password))
        print ' decrypting '+self.filename+' to '+output
        start = time.time()
        self.st.clear()
        self.st.settext("Encrypting .......")
        demo.AESdemo().encrypt_file( self.filename, output, password)
        end = time.time()    
        print('Time',end - start,'s')
        time_taken = 'Done! /nTime taken '+str(end - start)+'s'
        self.st.clear()
        self.st.settext(time_taken)       
        
    def Decrypt(self,result):
        print 'Decrypting file'+self.filename2+'.....'
        self.st.clear()
        self.st.settext("Encrypting .......")
        password = self.dpassword.getvalue()
        doutput = self.doutput.getvalue()
        print 'password: '+password
        print 'out put file: '+doutput
        start = time.time()        
        demo.AESdemo().decrypt_file( self.filename2, doutput, password)
        end = time.time()    
        print('Time',end - start,'s')
        msg = 'Decrypting file '+self.filename2+'.....'
        time_taken = msg+'/nTime taken '+str(end - start)+'s'
        self.st.clear()
        self.st.settext(time_taken)        
    
    def execute(self, result):
        if result is None or result == 'Cancel':
            print 'cancelled'
            self.dialog.deactivate()
        else:
            count = self.dialog.get()
            set_port = open("port.txt","w+")
            set_port.write("port,"+count)
            print("Serial port set to "+ count)
            st.settext("Serial port set to "+ count)
            set_port.close()
            self.dialog.deactivate()
    

#frame
frame = Frame(root,bg='#F2F3F4',borderwidth=12)

widget = App(frame)
frame.pack()

root.mainloop()
