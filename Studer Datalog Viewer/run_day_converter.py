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




file_path ='LG190130.CSV'
user_delimiter=';' 
day_datalog=xt_log_day_import(file_path, user_delimiter)




print(" _______  DISPLAY  _______ ")
print(" \n \n \n ")

chanel_number=0
batt_valmin=day_datalog['datalog_value'][:,chanel_number]
chanel_number=13
batt_val=day_datalog['datalog_value'][:,chanel_number]

minutes_of_the_day=day_datalog['time_minutes_of_the_day']

chanel_number=43
solar_power=day_datalog['datalog_value'][:,chanel_number]
chanel_number=31
VS_Upv=day_datalog['datalog_value'][:,chanel_number]



fig1=plt.figure(1)
plt.clf()
plt.plot(minutes_of_the_day/60, batt_val, 'b+-')
plt.plot(minutes_of_the_day/60, batt_valmin,'y+-')

plt.xlabel('Time (hours)', fontsize=12)
plt.ylabel('Voltage', fontsize=12)
plt.title('Battery Voltage', fontsize=14, weight="bold")
plt.ax = fig1.gca()
plt.ax.grid(True)




fig2, ax1 = plt.subplots()
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax1.plot(minutes_of_the_day/60, solar_power, 'r')
ax1.tick_params(axis='y', labelcolor='r')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('Power [kW]', fontsize=12, color='r')

#ax1.plot(minutes_of_the_day/60, solar_power)

color = 'tab:blue'
ax2.set_ylabel('Voltage', fontsize=12, color='b')  # we already handled the x-label with ax1
ax2.plot(minutes_of_the_day/60, VS_Upv,'b')
ax2.tick_params(axis='y', labelcolor='b')

fig2.tight_layout()

plt.ax = fig2.gca()
plt.ax.grid(True)


#fig2=plt.figure(2)
#plt.clf()
#
#plt.xlabel('Time (hours)', fontsize=12)
#plt.ylabel('Voltage', fontsize=12)
#plt.title('Solar Production and PV Voltage', fontsize=14, weight="bold")
#plt.ax = fig1.gca()
#plt.ax.grid(True)


plt.show()
