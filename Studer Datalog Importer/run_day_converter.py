"""
Created on Sun Feb 24 20:33:42 2019

  run_day_converter.py
  Version py 1.0   24 fevrier 2019
  Moix P-O
  WWW.OFFGRID.CH   Albedo-Engineering ALBEDO.CH
  
Simple test of fonction xt_log_day_import
"""


import matplotlib.pyplot as plt
import numpy as np

from xt_log_day_import import xt_log_day_import




file_path ='C:/Users/moix_/Dropbox/Python/StuderPy/Studer Datalog Importer/LG190130.CSV'
user_delimiter=';' 
day_datalog=xt_log_day_import(file_path, user_delimiter)




print(" _______  DISPLAY  _______ ")
print(" \n \n \n ")

chanel_number=0
batt_valmin=day_datalog['datalog_value'][:,chanel_number]
chanel_number=39
batt_val=day_datalog['datalog_value'][:,chanel_number]

minutes_of_the_day=day_datalog['time_minutes_of_the_day']





fig1=plt.figure(1)
plt.clf()
plt.plot(minutes_of_the_day/60, batt_val, 'b+-')
plt.plot(minutes_of_the_day/60, batt_valmin,'y+-')

plt.xlabel('Time (hours)', fontsize=12)
plt.ylabel('Voltage', fontsize=12)
plt.title('Battery Voltage', fontsize=14, weight="bold")
plt.ax = fig1.gca()
plt.ax.grid(True)

plt.show()
