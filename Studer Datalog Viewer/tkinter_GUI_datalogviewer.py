# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 23:01:42 2020

@author: moix_
@modified by: brycepg

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
import sys
from contextlib import contextmanager

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
from tkinter import scrolledtext


########################
# 1 Constants
########################

LARGE_FONT = ("Verdana", 12)
SYNOPT_VALUES_FONT = ("Verdana", 16, "bold")
# SYNOPTIC_IMAGE_SIZE=(1000, 596)
USED_ICON = "icone_albedo.ico"

style.use("ggplot")
DEBUG = False


########################
# 2 Functions
########################
@contextmanager
def redirect_console_output(new_io):
    """Redirect console output to the given IO object

    The given IO object must implement a write method
    which takes a string
    """
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = new_io
    sys.stderr = new_io
    try:
        yield None
    finally:
        sys.stdout = save_stdout
        sys.stderr = save_stderr


def popuphelp():
    # messagebox.showinfo("Help","blablablaaaa...")
    messagebox.showinfo(
        "Help",
        "Programm freely shared without support, please see my website and take contact if you think I can do something for you: wwww.albedo-engineering.com",
    )


def popuperror(message):
    messagebox.showinfo("Error", message)


def popup_about():
    """Create a separate window to show about page"""
    popup = tk.Toplevel()
    image = Image.open(USED_ICON)
    photo_image = ImageTk.PhotoImage(image)
    exit_button = ttk.Button(popup, text="Ok", command=popup.destroy)
    text_label = ttk.Label(popup, text="This is a datalog viewer for csv files...")
    image_label = tk.Label(popup, image=photo_image)

    # Ordering
    text_label.pack()
    image_label.pack(fill=tk.BOTH, expand=tk.YES)
    exit_button.pack()

    popup.mainloop()


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


class TransitionFrame(tk.Frame):
    """Frame for transitioning between frames

    The transition frame is needed to prevent
    the user from thinking the program has
    frozen while waiting for data to load
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self.tkraise()
        self.update()

    def build_progress_updater(self, text):
        """Build progress bar on transition frame

        Args:
            text: Text to display above the progress bar
            while loading happens
        """
        progress_bar_and_text_container = tk.Frame(self)
        progress_bar_and_text_container.grid()
        label = ttk.Label(progress_bar_and_text_container, text=text)
        label.pack()
        progress_bar = ttk.Progressbar(
            progress_bar_and_text_container,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            value=0,
        )
        progress_bar.pack()
        progress_bar.update()
        return ProgressUpdater(progress_bar, label)


def load_and_show_graphs(controller):
    """A callback to load the graph data when the graph frame is opened

    This callback needs to be partialed (curried) because of the argument
    """
    transition_frame = TransitionFrame(controller.frames[PageGraph].parent)
    try:
        progress_updater = transition_frame.build_progress_updater("Loading graphs")
        try:
            controller.frames[PageGraph].load_graphs_from_data(progress_updater)
        except Exception as exc:
            popuperror(f"Graph loading failed with '{exc}'")
            controller.show_frame(StartPage)
            return
        controller.show_frame(PageGraph)
    finally:
        # Cleanup
        transition_frame.destroy()




class DatalogVisuApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        tk_style = ttk.Style()

        if os.name == "nt":
            # The theme and icon fail to run on Linux because they are
            # Windows specific
            self.iconbitmap(USED_ICON)
            tk_style.theme_use("vista")
        tk_style.configure("TProgressbar", background="red")

        tk.Tk.wm_title(self, "Datalog Graph Viewer")

        self.geometry("1000x650")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
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
        helpmenu.add_command(label="About", command=popup_about)

        menubar.add_cascade(label="More", menu=helpmenu)

        #######
        # display the menu
        self.config(menu=menubar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def destroy(self):
        # Tkinter will hang and fail to exit if not all matplotlib plots are closed
        plt.close("all")
        super().destroy()


class ProgressUpdater:
    """Handle the updating of the progress bar"""
    def __init__(self, progress_bar, label):
        self.progress_bar = progress_bar
        self.cur_count = progress_bar["value"]
        self.label = label
        self.text = label["text"]

    def set_maximum_progress_value(self, number_of_increments):
        """Set the number of increments the progress bar should have"""
        self.progress_bar["maximum"] = number_of_increments

    def increment(self):
        """Increment the progress bar status"""
        self.progress_bar["value"] = self.cur_count+1
        self.progress_bar.update()
        self.cur_count += 1

    def set_subtext(self, subtext):
        self.label["text"] = f"{self.text}: {subtext}"
        self.label.update()


class TabConfiguration:
    """This is a data class for building a tab with a figure in it"""
    def __init__(self, func, func_args, title, parent):
        """
        Args:
            func: a function or method which returns a matplotlib figure
            func_args:
                a tuple containing the arguments for `func`
                We Don't call the function here because the function calls
                can take quite a bit of time, and want to show a progress
                bar between figures
            title:
                The title of the tkinter tab to show
            parent:
                The notebook to attach the figure to
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
        self.parent = parent

    def build_figure(self):
        """Apply the given arguments to the given function

        Returns:
            `self.func` result which should be a matplotlib `Figure` object
        """
        return self.func(*self.func_args)


class StartPage(tk.Frame):
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


class PageGraph(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        #pagetitle = tk.Label(self, text="Battery", font=LARGE_FONT)
        #pagetitle.pack(pady=10, padx=10)

        ######
        self.notebook = ttk.Notebook(self)  # Create notebook system
        self.notebook.pack()
        parent.update()
        self.system_notebook = self.build_categorical_tab("System")
        self.solar_notebook = self.build_categorical_tab("Solar")
        self.battery_notebook = self.build_categorical_tab("Battery")
        self.ac_notebook = self.build_categorical_tab("AC")
        # Keep track of created tabs
        self.tabs = []
        self.parent = parent

    def build_categorical_tab(self, text):
        """Build tabs which can hold other tabs"""
        tab = self.build_tab(text)
        # Frames can't have tabs so use a notebook
        # To allow for tabs to be attached
        categorical_notebook = ttk.Notebook(tab)
        categorical_notebook.pack()
        # Ctrl-tab shifts tabs
        categorical_notebook.enable_traversal()
        return categorical_notebook

    def build_tab(self, text, parent=None):
        """Build a tab for `parent` with `text as the title

        Returns a tkinter Frame which is a tab for
        the given notebook.

        Args:
            text: Text to display on tab
            parent: An optional notebook for the tab-frame to attach to
                If no parent is supplied, use the page graph main notebook
        """
        if parent is None:
            parent = self.notebook
        tab = ttk.Frame(parent)
        tab.pack()
        parent.add(tab, text=text)
        return tab

    def load_graphs_from_data(self, progress_updater):
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
                self.battery_notebook,
            ),
            TabConfiguration(
                build_battery_voltage_histogram_figure,
                (total_datalog_df, quarters_mean_df),
                "Histogram Voltage",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_ac_power_figure,
                (total_datalog_df, quarters_mean_df),
                "AC Power",
                self.ac_notebook,
            ),
            TabConfiguration(
                build_power_histogram_figure,
                (quarters_mean_df, total_datalog_df),
                "Histogram Power",
                self.system_notebook,
            ),
            TabConfiguration(
                build_voltage_versus_current_figure,
                (total_datalog_df,),
                "Volt vs Current",
                self.battery_notebook
            ),
            TabConfiguration(
                build_solar_production_figure,
                (total_datalog_df,),
                "Solar Production",
                self.solar_notebook
            ),
            TabConfiguration(
                build_genset_time_figure,
                (total_datalog_df,),
                "Genset Time",
                self.ac_notebook,
            ),
            TabConfiguration(
                build_all_battery_voltages_figure,
                (total_datalog_df, month_mean_df),
                "All Battery Voltages",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_montly_energies_figure,
                (total_datalog_df,),
                "Montly Energies",
                self.system_notebook,
            ),
            TabConfiguration(
                build_montly_energies_figure2,
                (total_datalog_df,),
                "Monthly Energies2",
                self.system_notebook,
            ),
        )

        progress_updater.set_maximum_progress_value(len(tab_configuration_seq))
        print("Building tabs")
        for i, tab_configuration in enumerate(tab_configuration_seq):
            if DEBUG:
                print(f"Tab i:{i}")
            progress_updater.set_subtext(f"Building {tab_configuration.title} graph")
            figure = tab_configuration.build_figure()
            self.attach_figure_to_new_tab(figure, tab_configuration.title, parent=tab_configuration.parent)
            progress_updater.increment()
        print("Done building tabs")

    def attach_figure_to_new_tab(self, figure, text, parent):
        """Attach the given `figure` to a new tab and attach that tab to the given `parent`

        Args:
            figure: A matplotlib figure
            text: The tab title text
            parent: A notebook which the tab will be attached to
        """
        tab = self.build_tab(text, parent=parent)
        self.attach_figure_to_tab(figure, tab)
        self.tabs.append(tab)

    def attach_figure_to_tab(self, figure, tab):
        """Attach a matplotlib figure to a tkinter tab"""
        canvas = FigureCanvasTkAgg(figure, tab)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        NavigationToolbar2Tk(canvas, tab)


class TextWidgetIOWriter:
    """Implements the write interface to replace stdout"""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, line):
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, line)
        # Automatically makes scrollbar scroll to the end
        self.text_widget.see("end")
        # Disable widget to disallow text to be written to it
        self.text_widget.configure(state="disabled")
        self.text_widget.update()


class PageLoadData(tk.Frame):
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

        text_widget = scrolledtext.ScrolledText(self)
        text_widget.configure(state="disabled")
        text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget = text_widget

    def load_data_from_filepath(self):
        """Call xt_all_csv_pandas_import from given filepath"""
        filepath = getfilepath()
        if filepath is None:
            return
        text_widget_io_writer = TextWidgetIOWriter(self.text_widget)
        # Delete to clear previous csv import calls
        self.text_widget.delete(0)
        with redirect_console_output(text_widget_io_writer):
            try:
                xt_all_csv_pandas_import.run(filepath)
            except Exception as exc:
                popuperror(f"The csv import script failed with '{exc}'")


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
