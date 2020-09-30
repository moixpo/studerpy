# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 23:01:42 2020

@author: moix_

Ressources and examples:
    -https://pythonprogramming.net/passing-functions-parameters-tkinter-using-lambda/?completed=/object-oriented-programming-crash-course-tkinter/
    -

"""

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

import xt_all_csv_pandas_import


########################
# 1 Constants
########################

LARGE_FONT = ("Verdana", 12)
SYNOPT_VALUES_FONT = ("Verdana", 16, "bold")
# SYNOPTIC_IMAGE_SIZE=(1000, 596)
USED_ICON = "icone_albedo.ico"

style.use("ggplot")


########################
# 2 Functions
########################


def popupinfo():
    messagebox.showinfo(
        "Infos about this", "This is an datalog viewer for csv files..."
    )


def popuphelp():
    # messagebox.showinfo("Help","blablablaaaa...")
    messagebox.showinfo(
        "Help",
        "Programm freely shared without support, please see my website and take contact if you think I can do something for you: wwww.albedo-engineering.com",
    )


def getfilepath():
    """Get the filepath for csv import from the user

    Returns:
        A file path to the selected file.
        If no file is selected return None
    """
    filepath = filedialog.askopenfilename(
        title="Choose an file",
        filetypes=(("csv files", ("*.csv", "*.CSV")), ("all files", "*.*")),
    )
    if not filepath:
        # An empty tuple will be returned if there is no file selected
        return None
    filename = os.path.split(filepath)[1]
    folder_path = os.path.split(filepath)[0]
    return filepath


class DatalogVisuApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        s = tk.ttk.Style()

        if os.name == "nt":
            # The theme and icon fail to run on Linux because they are
            # Windows specific
            tk.Tk.iconphoto(self, default=USED_ICON)
            s.theme_use("vista")

        tk.Tk.wm_title(self, "Datalog Graph Viewer")

        self.geometry("1000x650")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # All frames here MUST subclass ActivateFrame if they use self.show_frame
        for F in (StartPage, PageLoadData, PageGraph):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        # create a toplevel menu
        menubar = tk.Menu(self)

        # create a pulldown menu, and add it to the menu bar
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(
            label="Home Page", command=lambda: self.show_frame(StartPage)
        )
        filemenu.add_command(
            label="Load data", command=lambda: self.show_frame(PageLoadData)
        )
        filemenu.add_command(
            label="See graph", command=lambda: self.show_frame(PageGraph)
        )
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
        frame.activate()
        frame.tkraise()


class ActivateFrame(tk.Frame):
    def activate(self):
        """Hook to perform actions when the frame is active"""
        pass


class StartPage(ActivateFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.image = Image.open("snowflake.jpg")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind("<Configure>", self._resize_image)

        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(
            self,
            text="Import .csv files",
            command=lambda: controller.show_frame(PageLoadData),
        )
        button.place(relx=0.4, rely=0.5, anchor=tk.CENTER)

        #
        #        button2.pack()

        button3 = ttk.Button(
            self, text="Display graph", command=lambda: controller.show_frame(PageGraph)
        )

        button3.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
        # button3.pack()

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


class PageLoadData(ActivateFrame):
    """Handle loading of page data"""
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Load Data!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Select CSV file", command=self.load_data_from_filepath)
        button1.pack()

        button2 = ttk.Button(
            self, text="Display graph", command=lambda: controller.show_frame(PageGraph)
        )
        button2.pack()

        text_widget = tk.Text(self, width=50, height=10)
        text_widget.insert(tk.END, "Text to plot outputs and messages when importing")
        text_widget.pack()

    def load_data_from_filepath(self):
        filepath = getfilepath()
        if filepath is None:
            return
        # XXX: A progress bar may make sense here
        xt_all_csv_pandas_import.run(filepath)


class PageGraph(ActivateFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        pagetitle = tk.Label(self, text="Battery", font=LARGE_FONT)
        pagetitle.pack(pady=10, padx=10)

        ######
        self.notebook = ttk.Notebook(self)  # Create notebook system
        self.notebook.pack()

        self.voltage_current_tab = ttk.Frame(self.notebook)  # Add tab 1
        self.voltage_current_tab.pack()
        self.histogram_tab = ttk.Frame(self.notebook)  # Ajout de l'onglet 2
        self.histogram_tab.pack()
        self.daily_tab = ttk.Frame(self.notebook)  # Ajout de l'onglet 2
        self.daily_tab.pack()
        self.notebook.add(self.voltage_current_tab, text="Voltage-current")  # Name of tab 1
        self.notebook.add(self.histogram_tab, text="Histogramm Voltage")  # Name of tab 2
        self.notebook.add(self.daily_tab, text="Daily IN-OUT")  # Name of tab 3


    def activate(self):
        fig = generate_voltage_figure()
        canvas = FigureCanvasTkAgg(fig, self.voltage_current_tab)
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


def generate_voltage_figure():
    fig = Figure(figsize=(5, 5), dpi=100)
    ax1 = fig.add_subplot(2, 1, 1)

    ax1.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
    ax1.set_ylabel("Voltage [V]", fontsize=12)
    ax1.set_xlabel("Time", fontsize=12)
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
    ax2.set_ylabel("Current [V]", fontsize=12)
    ax2.set_xlabel("Time", fontsize=12)
    return fig


if __name__ == "__main__":
    app = DatalogVisuApp()
    app.mainloop()
