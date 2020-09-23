# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 23:01:42 2020

@author: moix_

Ressources and examples:
    -https://pythonprogramming.net/passing-functions-parameters-tkinter-using-lambda/?completed=/object-oriented-programming-crash-course-tkinter/
    -

"""


#import the necessary modules:

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt


import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from PIL import ImageTk, Image

import time
import datetime
import os


########################
#
# 1 Constants
#
########################
LARGE_FONT= ("Verdana", 12)
SYNOPT_VALUES_FONT=("Verdana", 16, 'bold')
#SYNOPTIC_IMAGE_SIZE=(1000, 596)
USED_ICON="icone_albedo.ico"

style.use("ggplot")



########################
#
# 2 Functions
#
########################

def popupinfo():
    messagebox.showinfo("Infos about this","This is an datalog viewer for csv files...")
    
def popuphelp():
    #messagebox.showinfo("Help","blablablaaaa...")
    messagebox.showinfo("Help","Programm freely shared without support, please see my website and take contact if you think I can do something for you: wwww.albedo-engineering.com")

def getfilepath():
    #file_path = filedialog.askopenfilename()
    file_path = filedialog.askopenfilename(initialdir="/", title="Choose an file",
                                       filetypes=(("csv files", "*.csv"),("all files", "*.*")))
    filename= os.path.split(file_path)[1]
    folder_path = os.path.split(file_path)[0]
    
    #filename = file_path.split('/')
    #panel = tk.Label(self, text= str(file_name[len(file_name)-1]).upper()).pack()
    #panel_image = tk.Label(self, image=img).pack()

        
    

class DatalogVisuApp(tk.Tk):
    
    
 

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=USED_ICON)

        tk.Tk.wm_title(self, "Datalog Graph Viewer")
        
        self.geometry("1000x650")
        
        
        s=tk.ttk.Style()
        #s.theme_names()'clam' 'vista'
        s.theme_use('vista')
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageLoadData, PageGraph):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        

        # create a toplevel menu
        menubar = tk.Menu(self)
        
        
        # create a pulldown menu, and add it to the menu bar
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Home Page", command=lambda: self.show_frame(StartPage))
        filemenu.add_command(label="Load data", command=lambda: self.show_frame(PageLoadData))
        filemenu.add_command(label="See graph", command=lambda: self.show_frame(PageGraph))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # create more pulldown menus        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=popuphelp)
        helpmenu.add_command(label="About", command=popupinfo)

        menubar.add_cascade(label="More", menu=helpmenu)
        
        #######
        # display the menu
        self.config(menu=menubar)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        self.image = Image.open("snowflake.jpg")
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind('<Configure>', self._resize_image)

     
        
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Import .csv files",
                            command=lambda: controller.show_frame(PageLoadData))
        button.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

#       
#        button2.pack()

        button3 = ttk.Button(self, text="Display graph",
                            command=lambda: controller.show_frame(PageGraph))
        
        button3.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
        #button3.pack()

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)
        
        

class PageLoadData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Load Data!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Select CSV file",
                            command=getfilepath)
        button1.pack()

        
        button2 = ttk.Button(self, text="Display graph",
                            command=lambda: controller.show_frame(PageGraph))
        button2.pack()

        text_widget = tk.Text(self,
                                   width=50, height=10)
        text_widget.insert(tk.END,
            "Text to plot outputs and messages when importing")
        text_widget.pack()


class PageGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        pagetitle = tk.Label(self, text="Battery", font=LARGE_FONT)
        pagetitle.pack(pady=10,padx=10)


        ######
        n = ttk.Notebook(self)   # Create notebook system
        n.pack()
        
        tab1 = ttk.Frame(n)       # Add tab 1
        tab1.pack()
        tab2 = ttk.Frame(n)       # Ajout de l'onglet 2
        tab2.pack()
        tab3 = ttk.Frame(n)       # Ajout de l'onglet 2
        tab3.pack()
        n.add(tab1, text='Voltage-current')      # Name of tab 1
        n.add(tab2, text='Histogramm Voltage')      # Name of tab 2
        n.add(tab3, text='Daily IN-OUT')      # Name of tab 3
        ###########
        

        

        #TODO:  To put on the tab....
        f = Figure(figsize=(5,5), dpi=100)
        
        #fig, (ax1, ax2) = plt.subplots(2, 1)
        
        ax1 = f.add_subplot(2,1,1)

        ax1.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        ax1.set_ylabel('Voltage [V]', fontsize=12)
        ax1.set_xlabel('Time', fontsize=12)
        ax2 = f.add_subplot(2,1,2)
        ax2.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        ax2.set_ylabel('Current [V]', fontsize=12)
        ax2.set_xlabel('Time', fontsize=12)


        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


#        labelscale = ttk.Label(self, text="Choose sampling rate", font=LARGE_FONT)
#        labelscale.pack(pady=10,padx=10)
#
#        scale_widget = ttk.Scale(self, from_=1, to=60,
#                                     orient=tk.HORIZONTAL)
#        scale_widget.set(5)
#        scale_widget.pack()
        


#        button1 = ttk.Button(self, text="Back to Home",
#                            command=lambda: controller.show_frame(StartPage))
#        button1.pack()
        

app = DatalogVisuApp()


app.mainloop()
       