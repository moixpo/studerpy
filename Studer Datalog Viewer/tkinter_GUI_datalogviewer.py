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
import types
import datetime
import os
from functools import partial

import xt_all_csv_pandas_import
from xt_graph_plotter_pandas import (
    build_total_battery_voltages_currents_figure,
    build_battery_voltage_histogram_figure,
    build_ac_power_figure,
    build_power_histogram_figure,
    build_voltage_versus_current_figure,
    build_solar_production_figure,
    build_genset_time_figure,
    build_all_battery_voltages_figure,
    build_montly_energies_figure,
    build_montly_energies_figure2,
)


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
    messagebox.showinfo("Infos about this", "This is an datalog viewer for csv files...")


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


def load_and_show_graphs(controller):
    """A callback to load the graph data when the graph frame is opened

    This callback needs to be partialed (curried) because of the argument
    """
    controller.frames[PageGraph].load_graphs_from_data()
    controller.show_frame(PageGraph)


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
        filemenu.add_command(label="Home Page", command=lambda: self.show_frame(StartPage))
        filemenu.add_command(label="Load data", command=lambda: self.show_frame(PageLoadData))

        filemenu.add_command(
            label="See graph",
            command=partial(load_and_show_graphs, self),
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

    def destroy(self):
        # Tkinter will hang and fail to exit if not all matplotlib plots are closed
        plt.close("all")
        super().destroy()


class ActivateFrame(tk.Frame):
    def activate(self):
        """Hook to perform actions when the frame is active"""
        pass


class TabConfiguration:
    """This is a data class for building a tab with a figure in it"""
    def __init__(self, func, func_args, title):
        """
        Args:
            func: a function which returns a matplotlib figure
            func_args:
                a tuple containing the arguments for `func`
                We Don't call the function here because the function calls
                can take quite a bit of time, and want to show a progress
                bar between figures
            title:
                The title of the tkinter tab to show
        """
        if not callable(func):
            raise TypeError("TabConfiguration func must be a callable")
        if not isinstance(func_args, (tuple, list)):
            raise TypeError("TabConfiguration func_args must be a container")
        if not isinstance(title, str):
            raise TypeError("TabConfiguration title must be text")
        self.func = func
        self.func_args = func_args
        self.title = title

    def build_figure(self):
        """Apply the given arguments to the given function

        Returns:
            `self.func` result which should be a matplotlib `Figure` object
        """
        return self.func(*self.func_args)


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
            self,
            text="Display graph",
            command=partial(load_and_show_graphs, controller),
        )

        button3.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
        # button3.pack()

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


class PageGraph(ActivateFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        pagetitle = tk.Label(self, text="Battery", font=LARGE_FONT)
        pagetitle.pack(pady=10, padx=10)

        ######
        self.notebook = ttk.Notebook(self)  # Create notebook system
        self.notebook.pack()

        # Keep track of created tabs
        self.tabs = []

    def build_tab(self, text):
        tab = ttk.Frame(self.notebook)
        tab.pack()
        self.notebook.add(tab, text=text)
        return tab

    def load_graphs_from_data(self):
        """Load matplotlib graphs from pickled pandas data and attach them to tabs"""
        for tab in self.tabs:
            # Destroy tabs to make way for new data
            tab.destroy()
        # Discard former matplotlib plots from memory
        plt.close("all")
        self.tabs = []

        total_datalog_df = pd.read_pickle(xt_all_csv_pandas_import.MIN_DATAFRAME_NAME)
        quarters_mean_df = pd.read_pickle(xt_all_csv_pandas_import.QUARTERS_DATAFRAME_NAME)
        month_mean_df = pd.read_pickle(xt_all_csv_pandas_import.MONTH_DATAFRAME_NAME)
        # year_mean_df = pd.read_pickle(xt_all_csv_pandas_import.YEAR_DATAFRAME_NAME)

        # This data structure loads each figure and supplies the the tab title in one

        # tab_configuration_seq is a tuple of TabConfiguration instances:
        tab_configuration_seq = (
            TabConfiguration(
                build_total_battery_voltages_currents_figure,
                (total_datalog_df,),
                "Voltage-current",
            ),
            TabConfiguration(
                build_battery_voltage_histogram_figure,
                (total_datalog_df, quarters_mean_df),
                "Histogram Voltage",
            ),
            TabConfiguration(
                build_ac_power_figure,
                (total_datalog_df, quarters_mean_df),
                "AC Power",
            ),
            TabConfiguration(
                build_power_histogram_figure,
                (quarters_mean_df, total_datalog_df),
                "Histogram Power",
            ),
            TabConfiguration(
                build_voltage_versus_current_figure,
                (total_datalog_df,),
                "Volt vs Current",
            ),
            TabConfiguration(
                build_solar_production_figure,
                (total_datalog_df,),
                "Solar Production",
            ),
            TabConfiguration(
                build_genset_time_figure,
                (total_datalog_df,),
                "Genset Time",
            ),
            TabConfiguration(
                build_all_battery_voltages_figure,
                (total_datalog_df, month_mean_df),
                "All Battery Voltages",
            ),
            TabConfiguration(
                build_montly_energies_figure,
                (total_datalog_df,),
                "Montly Energies",
            ),
            TabConfiguration(
                build_montly_energies_figure2,
                (total_datalog_df,),
                "Monthly Energies2",
            ),
        )

        for tab_configuration in tab_configuration_seq:
            figure = tab_configuration.build_figure()
            self.attach_figure_to_new_tab(figure, tab_configuration.title)

    def attach_figure_to_new_tab(self, figure, text):
        tab = self.build_tab(text)
        self.attach_figure_to_tab(figure, tab)
        self.tabs.append(tab)

    def attach_figure_to_tab(self, figure, tab):
        """Attach a matplotlib figure to a tkinter tab"""
        canvas = FigureCanvasTkAgg(figure, tab)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, tab)
        toolbar.update()


class PageLoadData(ActivateFrame):
    """Handle loading of page data"""

    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent)
        label = tk.Label(self, text="Load Data!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Select CSV file", command=self.load_data_from_filepath)
        button1.pack()

        button2 = ttk.Button(
            self,
            text="Display graph",
            command=partial(load_and_show_graphs, controller),
        )
        button2.pack()

        text_widget = tk.Text(self, width=50, height=10)
        text_widget.insert(tk.END, "Text to plot outputs and messages when importing")
        text_widget.pack()

    def load_data_from_filepath(self):
        """Call xt_all_csv_pandas_import from given filepath"""
        filepath = getfilepath()
        if filepath is None:
            return
        # TODO redirect output to message screen
        xt_all_csv_pandas_import.run(filepath)


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


def main():
    """Main entry point for the gui"""
    app = DatalogVisuApp()
    app.mainloop()


if __name__ == "__main__":
    main()
