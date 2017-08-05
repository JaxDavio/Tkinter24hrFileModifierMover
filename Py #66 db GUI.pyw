
## OS:             Windows 7             
## Python:         3.6.1
##

## Author:         David Jackson
##                 jaxdavio@yahoo.com
##
## Purpose:        To move only .txt files in db, modified in the last 24hrs,
##                 from folder 'A' to 'B' using the tkinter GUI and also
##                 give user the option to check the last modification time.
##                 (You'll need to modify 2 .txt files in given folder and
##                  "Save" for this program to work properly.)



import os
import shutil
import datetime as dt
from tkinter import *
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import sqlite3

connection = sqlite3.connect("modifiedFiles_database.db")
c = connection.cursor()
c.execute("CREATE TABLE IF NOT EXISTS ModifiedLog(col_lastuser INT)")

class Feedback:

    def __init__(self, master):

        master.title('Welcome!')
        master.resizable(False, False)
        master.configure(bg = '#e1d8b9')


## STYLE
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#e1d8b9')
        self.style.configure('TButton', background = '#e1d8b9')
        self.style.configure('TLabel', background = '#e1d8b9', font = ('Arial', 12))
        self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))
        self.style.configure('TButton', foreground = 'blue')

## HEADER

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()


        self.src_entry = StringVar()
        self.dest_entry = StringVar()

        
        self.logo = PhotoImage(file = 'python_logo.gif')
        ttk.Label(self.frame_header, image = self.logo).grid(row = 1, column = 0)
        ttk.Label(self.frame_header, text = 'Daily Modified File Mover\n', style = 'Header.TLabel').grid(row = 1, column = 3, padx = 10)
        ttk.Label(self.frame_header, text = 'Source:').grid(row = 4, column = 0, padx = 10)
        ttk.Label(self.frame_header, text = '\nDestination:\n').grid(row = 9, column = 0, padx = 10)

        ttk.Entry(self.frame_header, textvariable = self.src_entry, width = 46).grid(row = 4, column = 3, columnspan = 5, padx = 10)
        ttk.Entry(self.frame_header, textvariable = self.dest_entry, width = 46).grid(row = 9, column = 3, columnspan = 5, padx = 10)


        ttk.Button(self.frame_header, text = 'Browse', command = self.askSrcDirectory).grid(row = 4, column = 10, padx = 10)
        ttk.Button(self.frame_header, text = 'Browse', command = self.askDestDirectory).grid(row = 9, column = 10, padx = 10)

## CONTENT

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        self.org_entry = StringVar()
        self.mod_entry = StringVar()
        
        
        
        ttk.Label(self.frame_content, text = 'Oldest Original File').grid(row = 3, column = 1, padx = 10)
        ttk.Label(self.frame_content, text = 'Newest Modified File').grid(row = 3, column = 5, padx = 10)


        ttk.Entry(self.frame_content, textvariable = self.org_entry, width = 25).grid(row = 4, column = 1, rowspan = 10, padx = 10)
        ttk.Entry(self.frame_content, textvariable = self.mod_entry, width = 25).grid(row = 4, column = 5, rowspan = 10, padx = 10)
        

        ttk.Button(self.frame_content, text = 'Transfer\n   Files', command = self.transfer).grid(row = 6, column = 3, padx = 10)
        ttk.Button(self.frame_content, text = 'Clear', command = self.clear_textbox).grid(row = 20, column = 1, padx = 10)
        ttk.Button(self.frame_content, text = 'Quit', command = quit).grid(row = 20, column = 5, padx = 10)
        

        ttk.Label(self.frame_header, text = '\n').grid(row = 0, column = 3, padx = 10)    #Spacing
        ttk.Label(self.frame_header, text = '\n').grid(row = 3, column = 3, padx = 10)
        ttk.Label(self.frame_header, text = '\n').grid(row = 10, column = 3, padx = 10)
        ttk.Label(self.frame_content, text = '\n').grid(row = 21, column = 3, padx = 10)
        ttk.Label(self.frame_content, text = '\n').grid(row = 23, column = 3, padx = 10)


        self.lastuser_entry = StringVar()
        ttk.Button(self.frame_content, text = '    Last User \nModification:', command = self.get_last_time).grid(row = 22, column = 1, padx = 10)
        ttk.Entry(self.frame_content, textvariable = self.lastuser_entry, width = 40).grid(row = 22, column = 2, columnspan = 4, padx = 10)


 

## FUNCTIONS

    
    def askSrcDirectory(self):
      src = filedialog.askdirectory()
      self.src_entry.set(src)


    def askDestDirectory(self):
      dest = filedialog.askdirectory()
      self.dest_entry.set(dest)




    def transfer(self):
        src = self.src_entry.get()
        dest = self.dest_entry.get()


        now = dt.datetime.now()
        ago = now-dt.timedelta(minutes = 1440)
        print (now) 

        for fname in os.listdir(src):
            path = os.path.join(src, fname)

            st = os.stat(path)    
            
            mtime = dt.datetime.fromtimestamp(st.st_mtime)
            if mtime > ago and fname.endswith('.txt'):
                self.mod_entry.set('%s'%(fname))
                shutil.move(os.path.join(src,fname), os.path.join(dest,fname))
                c.execute("INSERT INTO ModifiedLog(col_lastuser) VALUES(?)", (now,))
                connection.commit()
            else:
                mtime > ago and fname.endswith('.txt')
                self.org_entry.set('%s'%(fname))
                print (mtime)


    def get_last_time(self):
        connection = sqlite3.connect("modifiedFiles_database.db")
        c = connection.cursor()
        c.execute('SELECT * FROM ModifiedLog ORDER BY col_lastuser DESC Limit 1')
        l_time = c.fetchone() 
        self.lastuser_entry.set(l_time) 
        connection.close()




    def clear_textbox(self):
        self.src_entry.set('')
        self.dest_entry.set('')
        self.org_entry.set('')
        self.mod_entry.set('')
        self.lastuser_entry.set('')
        



def main():

    root = Tk()

  ## CENTER  

    root.withdraw()
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth())/2
    y = (root.winfo_screenheight() - root.winfo_reqheight())/2
    root.geometry("+%d+%d" % (x, y))
    root.deiconify()
    
  ## CENTER

    feedback = Feedback(root)
    root.mainloop()


if __name__ == "__main__": main()
