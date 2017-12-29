import os
from tkFileDialog import askopenfilename
from Tkinter import *
from PIL import Image,ImageTk
from matplotlib import pyplot as plt
import global_file as gf


class gui():

  def __init__(self):
    self.root = Tk()
    self.root.title('Sudoku Grabber and Solver')
    self.root.geometry("1024x540+250+100")

    self.mf = Frame(self.root)
    self.mf.pack()

    self.f1 = Frame(self.mf, width=600, height=250)
    self.f1.pack(fill=X)
    #f2 = Frame(mf, width=600, height=250)
    #f2.pack()

    Label(self.f1,text="Select Your File").grid(row=0, column=0, sticky='e')
    self.entry = Entry(self.f1, width=50, textvariable='file_path')
    self.entry.grid(row=0,column=1,padx=2,pady=2,sticky='we',columnspan=25)
    Button(self.f1, text="Browse", command=self.open_file).grid(row=0, column=27, sticky='ew', padx=8, pady=4)
    Button(self.f1, text="Process Now", width=32, command=lambda: self.close()).grid(sticky='ew', padx=10, pady=10)
    self.root.mainloop()


  def close(self):
    self.root.destroy()
    gf.start(self.filename)


  def open_file(self):
      
      self.filename = askopenfilename(filetypes = (("ALL files", "*.*")
                                                               ,("Image files", "*.jpg") ))
      print self.filename
      self.entry.delete(0, END)
      self.entry.insert(0, self.filename)
      #img = ImageTk.PhotoImage(Image.open(self.filename))
      #panel = Label(root, image = img)
      #panel.pack(side = "bottom", fill = "both", expand = "yes")

gui()