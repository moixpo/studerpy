# -*- coding: utf-8 -*-
"""

@author: moix_
@modified by: brycepg


"""

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.sankey as sk


import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from PIL import ImageTk, Image

import time
import types
import traceback
#import datetime
#from datetime import datetime

import datetime as dt


import os
from functools import partial
import sys
from contextlib import contextmanager

import xt_all_csv_pandas_import
from xt_graph_plotter_pandas import (
    build_operating_mode_pies,
    build_total_battery_voltages_currents_figure,
    build_bsp_voltage_current_figure,
    build_bsp_soc_current_figure,
    build_battery_voltage_histogram_figure,
    build_battery_chargedischarge_histogram_figure,
    build_mean_battery_voltage_figure,
    build_batvoltage_profile,
    build_battery_temperature_figure,
    build_bat_inout_figure,
    build_ac_power_figure,
    build_ac_apparentpower_figure,
    build_sys_power_figure,
    build_consumption_profile,
    build_power_histogram_figure,
    build_solar_production_figure,
    build_solar_pv_voltage_figure,
    build_solar_energy_prod_figure,
    build_genset_time_figure,
    build_genset_VF_behaviour,
    build_genset_runtime,
    build_all_battery_voltages_figure,
    build_monthly_energies_figure2,
    build_monthly_energy_sources_fraction_figure,
    build_sankey_figure,
    build_daily_energies_figure,
    build_daily_energies_heatmap_figure,
    build_energyorigin_pie_figure,
    InteractiveFigure,
)
from tkinter import scrolledtext


########################
# 1 Constants
########################

LARGE_FONT = ("Verdana", 12)
SYNOPT_VALUES_FONT = ("Verdana", 16, "bold")
# SYNOPTIC_IMAGE_SIZE=(1000, 596)
USED_ICON = "media/icone_albedo.ico"
HELP_PICTURE="media/image_helppopup.jpg"

style.use("ggplot") #ggplot  seaborn bmh dark_background Solarize_Light2  seaborn-darkgrid
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
    textpopup=str("First you have to load some csv data then you can plot it... \n"+
               "You can see the day/month and year summary in the csvExport folder \n"+
               "Figures are in the FigureExport Folder \n"+
               "\n"+
               "Not all cases are well treated (with grid feeding, with external charger, ...) so always be critic about what you see...  \n"+
               "\n"+
               "\n"+
               "Programm freely shared without support! \n"+               
               "Please see our website and take contact us you think we can do something for you: wwww.offgrid.ch  \n \n"
               )

    messagebox.showinfo(
        "Help",
        textpopup
    )
#    messagebox.showinfo(
#        "Help",
#        "First you have to load some csv data then you can plot it... \n You can see the day/month and year summary in the csvExport folder \nFigures are in the FigureExport Folder \n  \nProgramm freely shared without support! \n Please see our website and take contact us you think we can do something for you: wwww.offgrid.ch  \n \n Not all cases are well treated (with grid feeding, with external charger, ...) so always be critic about what you see...  ",
#    )


def popuperror(message):
    messagebox.showinfo("Error", message)


def popup_about():
    """Create a separate window to show about page"""
    popup = tk.Toplevel()
    image = Image.open(HELP_PICTURE)
    photo_image = ImageTk.PhotoImage(image)
    exit_button = ttk.Button(popup, text="Ok", command=popup.destroy)
    text_label = ttk.Label(popup, text="\n This is a datalog viewer for csv files recorded on Studer energy systems... \n ")
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
            print(traceback.format_exc())
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

        self.geometry("1000x720")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PageGraph, PageLoadData, StartPage):

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
            label="See graphs",
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

        self.image = Image.open("media/first_page_background.jpg")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind("<Configure>", self._resize_image)

        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        boldStyle = ttk.Style ()
        boldStyle.configure("Bold.TButton", font = ('Verdana','11','bold'))
        
        button = ttk.Button(
            self,
            text="Import .csv files",
            style= "Bold.TButton",
            command=lambda: controller.show_frame(PageLoadData),
        )
        button.place(relx=0.4, rely=0.5, anchor=tk.CENTER,
            height = 60, 
            width = 150)

        #
        #        button2.pack()

        button3 = ttk.Button(
            self,
            text="Display graph",
            style= "Bold.TButton",
            command=partial(load_and_show_graphs, controller),
        )

        button3.place(relx=0.6, rely=0.5, anchor=tk.CENTER,
            height = 60, 
            width = 150)
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
        self.system_notebook = self.build_categorical_tab("System Overview")
        self.consumption_notebook = self.build_categorical_tab("Consumption")
        self.solar_notebook = self.build_categorical_tab("Solar")
        self.battery_notebook = self.build_categorical_tab("Battery")
        self.gridgenset_notebook = self.build_categorical_tab("Grid/Genset")
        self.interactive_notebook = self.build_categorical_tab("INTERACTIVE")

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
        
        #means
        quarters_mean_df = pd.read_pickle(xt_all_csv_pandas_import.QUARTERS_DATAFRAME_NAME)
        day_mean_df = pd.read_pickle(xt_all_csv_pandas_import.DAY_DATAFRAME_NAME)
        month_mean_df = pd.read_pickle(xt_all_csv_pandas_import.MONTH_DATAFRAME_NAME)
        year_mean_df = pd.read_pickle(xt_all_csv_pandas_import.YEAR_DATAFRAME_NAME)
        
        
        #sums for energies:
        day_kwh_df=pd.read_pickle(xt_all_csv_pandas_import.DAY_KWH_DATAFRAME_NAME)
        month_kwh_df=pd.read_pickle(xt_all_csv_pandas_import.MONTH_KWH_DATAFRAME_NAME)
        year_kwh_df=pd.read_pickle(xt_all_csv_pandas_import.YEAR_KWH_DATAFRAME_NAME)

#TODO: REMOVEIT

        #For tests!!
        start_date = dt.date(2018, 7, 1)
        end_date = dt.date(2018, 8, 30)
        
        #start_date = dt.date(2018, 10, 1)
        #end_date = dt.date(2018, 10, 30)
#TODO: REMOVEIT



        # This data structure loads each figure and supplies the the tab title in one
        # tab_configuration_seq is a tuple of TabConfiguration instances:
        tab_configuration_seq = (
            TabConfiguration(
                build_consumption_profile,
                (total_datalog_df,),
                "Consumption INTERACT",
                self.interactive_notebook,
            ),
            TabConfiguration(
                build_sankey_figure,
                (day_kwh_df,),
                "Sankey INTERACT",
                self.interactive_notebook,
            ),
            TabConfiguration(
                build_power_histogram_figure,
                (total_datalog_df,quarters_mean_df),
                "hist INTERACT",
                self.interactive_notebook,
            ),
            TabConfiguration(
                build_batvoltage_profile,
                (total_datalog_df,),
                "Voltage INTERACT",
                self.interactive_notebook,
            ),
            TabConfiguration(
                build_energyorigin_pie_figure,
                (day_kwh_df,),
                "Origin Energy INTERACT",
                self.interactive_notebook,
            ),
            TabConfiguration(
                build_genset_time_figure,
                (total_datalog_df,),
                "Gen/Grid INTERACT",
                self.interactive_notebook,
            ),
            TabConfiguration(
                build_mean_battery_voltage_figure,
                (total_datalog_df,month_mean_df,day_mean_df),
                "Voltage means",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_bsp_voltage_current_figure,
                (total_datalog_df,),
                "BSP voltage-current",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_bsp_soc_current_figure,
                (total_datalog_df,),
                "BSP SOC-current",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_bat_inout_figure,
                (day_kwh_df, month_kwh_df,),
                "Throughput",
                self.battery_notebook,
            ), 
            TabConfiguration(
                build_battery_voltage_histogram_figure,
                (total_datalog_df, quarters_mean_df),
                "Histogram Voltage",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_battery_chargedischarge_histogram_figure,
                (total_datalog_df, quarters_mean_df),
                "Histogram Discharge/Charge",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_battery_temperature_figure,
                (quarters_mean_df,),
                "Temperature",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_total_battery_voltages_currents_figure,
                (total_datalog_df,),
                "All voltages-currents",
                self.battery_notebook,
            ),
            TabConfiguration(
                build_all_battery_voltages_figure,
                (total_datalog_df, month_mean_df),
                "All Battery Voltages",
                self.battery_notebook,
            ),                              
            TabConfiguration(
                build_genset_time_figure,
                (total_datalog_df,),
                "Connection Time",
                self.gridgenset_notebook,
            ),
            TabConfiguration(
                build_genset_runtime,
                (day_kwh_df,month_kwh_df,),
                "Hours per day/month",
                self.gridgenset_notebook,
            ),        
            TabConfiguration(
                build_genset_VF_behaviour,
                (total_datalog_df,),
                "AC-source V-F with power",
                self.gridgenset_notebook,
            ),
            TabConfiguration(
                build_monthly_energies_figure2,
                (month_kwh_df,),
                "Monthly Energies",
                self.system_notebook,
            ), 
            TabConfiguration(
                build_sankey_figure,
                (day_kwh_df,),
                "Sankey",
                self.system_notebook,
            ),
            TabConfiguration(
                build_monthly_energy_sources_fraction_figure,
                (month_kwh_df,),
                "Origin of energy",
                self.system_notebook,
            ),    
            TabConfiguration(
                build_daily_energies_figure,
                (day_kwh_df,),
                "Daily Energies",
                self.system_notebook,
            ),  
            TabConfiguration(
                build_sys_power_figure,
                (total_datalog_df,quarters_mean_df),
                "System powers",
                self.system_notebook,
            ), 
            TabConfiguration(
                build_power_histogram_figure,
                (total_datalog_df,quarters_mean_df),
                "Histogram Power",
                self.system_notebook,
            ),
            TabConfiguration(
                build_solar_energy_prod_figure,
                (total_datalog_df,day_kwh_df,month_kwh_df,),
                "Solar energy production",
                self.solar_notebook
            ),
            TabConfiguration(
                build_solar_production_figure,
                (total_datalog_df,),
                "PV power",
                self.solar_notebook
            ),
            TabConfiguration(
                build_solar_pv_voltage_figure,
                (total_datalog_df,),
                "PV voltage",
                self.solar_notebook
            ),        
            TabConfiguration(
                build_operating_mode_pies,
                (total_datalog_df,),
                "Operation",
                self.system_notebook,
            ),
            TabConfiguration(
                build_daily_energies_heatmap_figure,
                (day_kwh_df,),
                "Daily Energies Map",
                self.consumption_notebook,
            ),
            TabConfiguration(
                build_ac_power_figure,
                (total_datalog_df, quarters_mean_df),
                "All active powers",
                self.consumption_notebook,
            ),
            TabConfiguration(
                build_ac_apparentpower_figure,
                (total_datalog_df, quarters_mean_df),
                "AC-peak powers",
                self.consumption_notebook,
            ),
            TabConfiguration(
                build_consumption_profile,
                (total_datalog_df, ),
                "Consumption profile",
                self.consumption_notebook,
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
        if isinstance(figure, InteractiveFigure):
            figure.attach_to_tab(tab)
        else:
            plt.close(figure)
            self.attach_figure_to_tab(figure, tab)
        self.tabs.append(tab)


    def attach_figure_to_tab(self, figure, tab):
        """Attach a matplotlib figure to a tkinter tab"""
        canvas = FigureCanvasTkAgg(figure, tab)
        #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        #NavigationToolbar2Tk(canvas, tab)

        #TODO: fix problem with toolbar hiden with figure size: not OK when resizing
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, tab)
        toolbar.update()
        #toolbarFrame = tk.Frame(master=window)
        #toolbarFrame.grid(row=2,column=0)
        #toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


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
        label = tk.Label(self, text="Load Data: select the first valid .csv file, \n all dates after this one will be processed", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        #TODO: add pic for the button
        #photo_csv = tk.PhotoImage(file="loadcsv.png")
        
        #buttonImage = tk.Image.open('loadcsv.png')
        #self.buttonPhoto = tk.ImageTk.PhotoImage(buttonImage)
        #myButton = ttk.Button(self, image=buttonPhoto, padding='10 10 10 10')
         
        #photo_csv=tk.PhotoImage(file="loadcsv.png")
        #button1 = ttk.Button(self, text="Select CSV file", image=photo_csv, command=self.load_data_from_filepath, height=100, width=200)        
        #button1 = ttk.Button(self, text="Select CSV file", image=photo_csv, command=self.load_data_from_filepath)
        
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






def main():
    """Main entry point for the gui"""
    
    #USE LIMITER... in case of...    
    now = dt.datetime.now()
    #print(dt.utcnow())
    print('This month is ', now.month, 'in the year ' ,now.year)
    if now.year>=2021:
        if now.month>=12:
            print('Time has gone... so fast')
            while True:
                #do nothing
                print('You are in a black hole')
    #    else:
    #        print('Enjoy life')
    #else:
    #    print('Enjoy life')
                
            
    app = DatalogVisuApp()
    app.mainloop()


if __name__ == "__main__":
    main()
