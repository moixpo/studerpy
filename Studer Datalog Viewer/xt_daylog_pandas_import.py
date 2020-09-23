###################################
#  xt_daylog_pandas_import.py
#  Version py 1.0   june 2020
#  Moix P-O
#  WWW.OFFGRID.CH    Albedo-Engineering ALBEDO.CH
#
#  License GPL-3.0-only ou GPL-3.0-or-later

  
######################
# DESCRIPTION
#
#   Function to import Studer-Innotec datalog .csv file.
#
#   xt_log_day_importer(filename, user_delimiter=',')
#

#######
# INPUTS:
#   filename: name of the log file: LG091006.CSV per example, give the full path if not in the same folder
#
#   user_delimiter=','      for english Excel display (used by default)
#   user_delimiter=';'      for french Excel
#
#

#######
# OUTPUTS:
#The returned DAY_DATALOG is a structure/dictionnary with the following fields
#
#   day_datalog =
#            'channels_label': 1xn list             name of the n channels logged
#              'day_of_month': 6                    day of the month
#                     'month': 10                   month of the year
#                      'year': 2009                 year
#   'time_minutes_of_the_day': 1x1440 double      time in minutes of the logged day.
#             'datalog_value': n x1440 double     n channels one point per day in a numpy array.
#           'version_datalog':'v6.10'               To see if an update was done in the middle.
#               'other_infos':                      Text available at the end of te datalog, kept for further treatments.



#%reset y
#%timeit


#import scipy
#from scipy import *
#from scipy.optimize import differential_evolution

#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import csv
#import time


#studer_datalog_day_converter(file_path,',')

def xt_daylog_pandas_import(file_path, user_delimiter=',', offsetcolumn=0):
    
    mydateparser=lambda x: pd.datetime.strptime(x, "%d.%m.%Y %H:%M")
    pandatest = pd.read_csv(file_path, 
                            encoding="ISO-8859-1", 
                            delimiter=user_delimiter,
                            header=[0,1,2],
                            nrows=1440,
                            parse_dates=True,
                            date_parser=mydateparser,
                            index_col=0,
                            engine='python')  
    
    #index_col=0,   index_col=False , index_col=None
    #encoding="cp1252" "utf-8"
    #skiprows=range(1, 10))
    # engine='c'
    
    
    
#    print(pandatest.head(5))
#    print(" ")
#    pandatest.iloc[[2], [3]] #point one element to see
#    pandatest.index  #to see the time index of each line
#    pandatest.columns #to see the label of each column
    
    
    #theres is a unexplanable shift with the labels of columns with xt logs
    # no explaination yet: turn around to avoid it with an offset
    #merge of the first three lines of headers:
    
    
    newlabels=[]
    for elem in list(pandatest.columns[offsetcolumn:]):
        #print(elem[0] + ' ' +elem[1] + ' ' + elem[2])
        newlabels.append(elem[0] + ' ' +elem[1] + ' ' + elem[2])
        #pandatest.columns[1:]
        
    
    #selected_columns = pandatest.columns[0:len(pandatest.columns)-2]
    
    
    datalog_values=pandatest.values[:,0:len(newlabels)]
    #datalog_values[:,0:len(newlabels)]
    
    
    daylog_df= pd.DataFrame(datalog_values,
                            index=pandatest.index,
                            columns=newlabels)

    return daylog_df
    
