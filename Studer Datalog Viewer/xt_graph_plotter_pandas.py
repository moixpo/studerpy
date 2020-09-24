# -*- coding: utf-8 -*-
"""
#  Version  2.2  sept 2020
#  Moix P-O
#  Albedo-Engineering WWW.ALBEDO-ENGINEERING.COM
#  WWW.OFFGRID.CH   
#  License GPL-3.0-only ou GPL-3.0-or-later
  
xt_graph_plotter_pandas.py
  
"""



import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_name='saved_dataframe_log_min'
total_datalog_df = pd.read_pickle(file_name)
file_name='saved_dataframe_log_quarters'
quarters_mean_df=pd.read_pickle(file_name) 

file_name='saved_dataframe_log_day'
day_mean_df = pd.read_pickle(file_name)
file_name='saved_dataframe_log_month'
month_mean_df = pd.read_pickle(file_name)
file_name='saved_dataframe_log_year'
year_mean_df = pd.read_pickle(file_name)


#%***************************************
#% task: compute kWh
# WARNING: it make sense only for P in KW
#TODO: make a dataframe for energies
#%****************************************

#min to day: *60*24/1000
#day to month: *60*24/1000

day_kwh_df=total_datalog_df.resample("1d").sum()/60
month_kwh_df=total_datalog_df.resample("1M").sum()/60
year_kWh_df=total_datalog_df.resample("1Y").sum()/60

    


#close all existing figures at start
plt.close("all")


    
print(" ")
print(" __________ GRAPH DISPLAY  _______________ ")
print(" \n \n \n ")





channels_labels=list(total_datalog_df.columns)


################################
#plot all the channels with battery voltage and current:
chanels_number_ubat = [i for i, elem in enumerate(channels_labels) if 'Ubat' in elem]
chanels_number_ibat = [i for i, elem in enumerate(channels_labels) if 'Ibat' in elem]

#fig_bat=plt.figure()
fig_batt, (axes_bat_u,axes_bat_i) = plt.subplots(nrows=2, ncols=1)

total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_ubat],
                      grid=True,
                      figsize=(15,5),
                      sharex=True,
                      ax=axes_bat_u)

axes_bat_u.set_ylabel('Voltage [V]', fontsize=12)
axes_bat_u.set_title('All Battery Voltages', fontsize=12, weight="bold")
axes_bat_u.grid(True)
plt.show

total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_ibat],
                      figsize=(15,5),
                      grid=True,
                      sharex=True,
                      ax=axes_bat_i)

axes_bat_i.set_ylabel('Amperes [A]', fontsize=12)
axes_bat_i.set_title('All Battery Currents', fontsize=12, weight="bold")
axes_bat_i.grid(True)



fig_batt_hist, axes_bat_u_hist = plt.subplots(nrows=1, ncols=1)

quarters_mean_df.plot(y=quarters_mean_df.columns[chanels_number_ubat[1]],
                      figsize=(12,6),
                      kind='hist',
                      bins=40,
                      ax=axes_bat_u_hist)

axes_bat_u_hist.set_xlabel('Voltage [V]', fontsize=12)
axes_bat_u_hist.set_ylabel('occurence', fontsize=12)
axes_bat_u_hist.set_title('Battery Voltage Histogramm', fontsize=12, weight="bold")
axes_bat_u_hist.grid(True)















######################################
#plot all the channels with Power 
chanels_number_Pactif = [i for i, elem in enumerate(channels_labels) if '[kW]' in elem]
chanels_number_Papparent = [i for i, elem in enumerate(channels_labels) if '[kVA]' in elem]

#fig100=plt.figure(100)
fig_pow, axes_pow = plt.subplots(nrows=1, ncols=2)

total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_Pactif],
                      figsize=(12,6),
                      ax=axes_pow[0])

axes_pow[0].set_ylabel('Power activ/reactiv [kW/kVA]', fontsize=12)
axes_pow[0].set_title('All AC-out Powers', fontsize=12, weight="bold")
axes_pow[0].grid(True)



total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_Papparent],
                      marker='+',
                      figsize=(12,6),
                      ax=axes_pow[1])
quarters_mean_df.plot(y=quarters_mean_df.columns[chanels_number_Papparent],
                      marker='o',
                      ax=axes_pow[1])
axes_pow[1].set_ylabel('Power apparent [kVA]', fontsize=12)
axes_pow[1].set_title('1min and 15min AC-out Power', fontsize=12, weight="bold")
axes_pow[1].grid(True)





fig_hist, axes_hist = plt.subplots()
quarters_mean_df.plot(y=quarters_mean_df.columns[chanels_number_Pactif[0]],
                      figsize=(12,6),
                      kind='hist',
                      bins=20,
                      ax=axes_hist)

axes_hist.set_title('Histogramm of Powers', fontsize=12, weight="bold")
axes_hist.set_xlabel('Power', fontsize=12)

axes_hist.grid(True)









######################
# Battery analysis 
######
chanels_number_ubatbsp = [i for i, elem in enumerate(channels_labels) if 'BSP-Ubat' in elem]
chanels_number_ibatbsp = [i for i, elem in enumerate(channels_labels) if 'BSP-Ibat' in elem]


fig_batt, axes_batt = plt.subplots(nrows=1, ncols=1)
axes_batt.scatter(total_datalog_df.values[:,chanels_number_ibatbsp],total_datalog_df.values[:,chanels_number_ubatbsp])

axes_batt.set_xlabel('Amperes [A]', fontsize=12)
axes_batt.set_ylabel('Voltage [V]', fontsize=12)
axes_batt.set_title('Voltage VS Currents', fontsize=12, weight="bold")
axes_batt.grid(True)


#######
## Charge /discharge power
########
battery_power=total_datalog_df.values[:,chanels_number_ubatbsp]*total_datalog_df.values[:,chanels_number_ibatbsp]/1000

#battery_power_df=pd.DataFrame({"Battery Power [kW]": battery_power,
#                               "Battery Charge Power [kW]": battery_power,
#                               "Battery Discharge Power [kW]": battery_power},
#                                index=total_datalog_df.index)
#                               
#                               


#plt.show

##########
#Solar Power:
############
chanel_number_for_solar=[i for i, elem in enumerate(channels_labels) if 'Solar power (ALL) [kW]' in elem]

fig_solar, axes_solar = plt.subplots(nrows=1, 
                           ncols=1,
                           figsize=(15,5))

total_datalog_df.plot(y=total_datalog_df.columns[chanel_number_for_solar],
                      figsize=(12,6),
                      ax=axes_solar)
axes_solar.set_ylabel('Power [kW]', fontsize=12)
axes_solar.set_title('Solar Production', fontsize=12, weight="bold")
axes_solar.grid(True)


##########
#Time on the genset:
############


chanel_number_for_transfer=[i for i, elem in enumerate(channels_labels) if 'XT-Transfert' in elem]
minutes_without_transfer=np.count_nonzero(total_datalog_df.values[:,chanel_number_for_transfer] == 0.0) 
minutes_with_transfer=np.count_nonzero(total_datalog_df.values[:,chanel_number_for_transfer] == 1.0)
 
len(total_datalog_df.values[:,chanel_number_for_transfer])

labels = ['on grid/genset: ' +str(round(minutes_with_transfer/60,1)) + ' hours',
          'on inverter: ' +str(round(minutes_without_transfer/60,1)) + ' hours']
fig_transfer=plt.figure()
ax_transfer=fig_transfer.add_subplot(111)
ax_transfer.pie([minutes_with_transfer,minutes_without_transfer],
        labels=labels,
        shadow=True, 
        startangle=90,
        autopct='%1.1f%%')
        
#plt.show()



#Analyse Batterie


fig_batt_anlys, axes_batt_anlys = plt.subplots(nrows=1, 
                           ncols=1,
                           figsize=(15,5))
#axes4_2 = axes4.twinx()

total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_ubat],
                      figsize=(15,5),
                      grid=True,
                      title='All Battery Voltages',
                      ax=axes_batt_anlys)

month_mean_df.plot(y=month_mean_df.columns[chanels_number_ubat[1]],
                      color='r',
                      ax=axes_batt_anlys)

axes_batt_anlys.set_ylabel('Voltage [V]', fontsize=12)
axes_batt_anlys.set_title('All Battery Voltages', fontsize=12, weight="bold")
axes_batt_anlys.grid(True)

#axes4.bar(x=month_mean_df.index, 
#        y=total_datalog_df.columns[chanels_number_ubat],
#        color='r',
#        ax=axes4_2)
#
#axes4.plot(x=total_datalog_df.index,
#         y=total_datalog_df.columns[chanels_number_ubat],
#         grid=True,
#         title='All Battery Voltages',
#         ax=axes4)





#Energies Mensuelles:

#month_kwh_df['XT-Pout a [kW] I3101 L1-1']
fig_ener, axes_ener = plt.subplots(nrows=1, 
                           ncols=1,
                           figsize=(15,5))




#month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
#                      kind='line',
#                      marker='o',
#                      color='red',
#                      ax=axes_ener)

month_kwh_df[['Solar power (ALL) [kW] I17999 ALL','XT-Pin a [kW] I3119 L1-1','XT-Pout a [kW] I3101 L1-1']].plot.bar(grid=True,
                      stacked=False,
                      ax=axes_ener)

axes_ener.set_ylabel('Energy [kWh]', fontsize=12)
axes_ener.set_title('Energies Mensuelles', fontsize=12, weight="bold")
axes_ener.grid(True)

plt.show()


fig_ener2, axes_ener2 = plt.subplots(nrows=1, 
                           ncols=1,
                           figsize=(9,9))



month_kwh_df[['Solar power (ALL) [kW] I17999 ALL','XT-Pin a [kW] I3119 L1-1']].plot.bar(stacked=True,
                      ax=axes_ener2,
                      use_index=False,
                      align='edge',
                      width=0.5)


month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(kind='bar',
                      color='red',
                      align='center',
                      width=0.5,
                      ax=axes_ener2,
                      use_index=False)

month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(kind='line',
                      marker='o',
                      color='red',
                      ax=axes_ener2,
                      use_index=False)


axes_ener2.set_ylabel('Energy [kWh]', fontsize=12)

#replace labels with the month name:
loc, label= plt.xticks()
plt.xticks(loc,labels=list(month_kwh_df.index.month_name()) )

axes_ener2.set_title('Energies Mensuelles', fontsize=12, weight="bold")
axes_ener2.grid(True)






#######
## HEAT MAPS:  TODO
########
#https://scipython.com/book/chapter-7-matplotlib/examples/a-heatmap-of-boston-temperatures/
#https://vietle.info/post/calendarheatmap-python/






#









##minimal battery voltage
#chanel_number=single_days['channels_label'].index('XT-Ubat- (MIN) [Vdc]') 
#XT_batt_valmin=total_datalog_value[:,chanel_number]
#
##battery voltage
#chanel_number=single_days['channels_label'].index('XT-Ubat [Vdc]') 
#XT_batt_val=total_datalog_value[:,chanel_number]
#
#
#chanel_number=single_days['channels_label'].index('BSP-Ubat [Vdc]') 
#BSP_batt_val=total_datalog_value[:,chanel_number]
#
#chanel_number=single_days['channels_label'].index('BSP-Ibat [Adc]') 
#BSP_I_batt_val=total_datalog_value[:,chanel_number]
#
##'BSP-Ubat [Vdc]',
## 'BSP-Ibat [Adc]',
## 'BSP-SOC [%]',
## 'BSP-Tbat [°C]',
# 
#
#
#chanel_number=single_days['channels_label'].index('XT-Pin a [kW]') 
#grid_power=total_datalog_value[:,chanel_number]
#
#   
#print(" ************* ")
#print("BEWARE: for 3-phased systems, the sum of the three inverters")
#grid_power=total_datalog_value[:,chanel_number]+total_datalog_value[:,chanel_number+1]+total_datalog_value[:,chanel_number+2]
#print(" comment this line if not the case ")
#print(" ************* ")
#print("  ")
#minutes_of_the_day=total_time_vectors
#
#
#
#
#fig1=plt.figure(1)
#plt.clf()
#plt.plot(minutes_of_the_day/60/24, XT_batt_val, 'b')
#plt.plot(minutes_of_the_day/60/24, BSP_batt_val, 'g')
#plt.plot(minutes_of_the_day/60/24, XT_batt_valmin,'y+-')
#
#plt.xlabel('Time (days)', fontsize=12)
#plt.ylabel('Voltage [V]', fontsize=12)
#plt.title('Battery Voltage', fontsize=18, weight="bold")
#
#plt.ax = fig1.gca()
#plt.ax.grid(True)
#
#plt.show()
#fig1.legend(['mesure XT', 'mesure BSP', 'xt min'])
#
#
#fig2=plt.figure(2)
#plt.clf()
#plt.hist(BSP_batt_val, 25, facecolor='r', alpha=0.75)
#
#plt.xlabel('Voltage [V]')
#plt.ylabel('Occurence')
#plt.title('Histogram of Battery Voltage')
#
##plt.text(52, 25, r'$\mu=100,\ \sigma=15$')
##plt.axis([40, 60, 0, 0.03])
#plt.grid(True)
#plt.show()
#
#plt.ax = fig2.gca()
#plt.ax.grid(True)
#
#
#