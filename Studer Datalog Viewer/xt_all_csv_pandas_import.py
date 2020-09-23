# -*- coding: utf-8 -*-
"""
#  Version  2.1  june 2020
#  Moix P-O
#  Copyright Albedo-Engineering WWW.ALBEDO-ENGINEERING.COM
# 
  
xt_datalog_viewer_pandas.py
  
"""



#reset of the workspace and close all existing figures
#from IPython import get_ipython
#get_ipython().magic('reset -sf') 
#separate figures: %matplotlib qt


#import the necessary modules:
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.collections as collections

import tkinter as tk
from tkinter import filedialog
#import datetime
import time
import os


#import the function to convert each datalog file:
#from xt_log_day_import import xt_log_day_import
from xt_daylog_pandas_import import xt_daylog_pandas_import



#close all existing figures at start
plt.close("all")


#OPTIONS:
user_delimiter=','  # ',' for english Excel display and ';' for french Excel option change in the RCC
#user_delimiter=';'  # ',' for english Excel display and ';' for french Excel option change in the RCC
#print('In case of error: have you checked the .csv delimiter? ')

user_delimiter='[,|;]'  # for all types of files. work only with python engine in csv_read, to accelerate and use c engine, use a single delimiter



#***************************************
# task 1: Choose the first .csv file
#****************************************

#the dialog window to select the first file to import:
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
filename= os.path.split(file_path)[1]
folder_path = os.path.split(file_path)[0]

##the old way:
#file_path_split=file_path.split('/')
#filename=file_path_split[len(file_path.split('/'))-1]
#folder_path=file_path[:-12]


#path_name=file_path_split[0:len(file_path.split('/'))-1]
# format LG180402.CSV

#The date is at the end of the name:
year_f=filename[-10:-8]
month_f=filename[-8:-6]
day_f=filename[-6:-4]
headfilename=filename[:-10]

print(file_path)


#timing to optimize the code:
start_time = old_time= time.time()




#### TESTS of imports with pandas: 
#
#mydateparser=lambda x: pd.datetime.strptime(x, "%d.%m.%Y %H:%M")
#
#pandatest = pd.read_csv(file_path, 
#                        encoding="ISO-8859-1", 
#                        delimiter=user_delimiter,
#                        header=[0,1,2],
#                        nrows=1440,
#                        parse_dates=True,
#                        date_parser=mydateparser,
#                        index_col=0,
#                        engine='c')  
#
##index_col=0,   index_col=False , index_col=None
##encoding="cp1252" "utf-8"
##skiprows=range(1, 10))
#
#
#
#print(pandatest.head(5))
#print(" ")
#pandatest.iloc[[2], [3]] #point one element to see
#pandatest.index  #to see the time index of each line
#pandatest.columns #to see the label of each column
#
##theres is a unexpllanable shift with the labels of colums,
## no explaination, turn around to avoid it
##merge of the first three lines of headers:
#
#
#newlabels=[]
#for elem in list(pandatest.columns[1:]):
#    print(elem[0] + ' ' +elem[1] + ' ' + elem[2])
#    newlabels.append(elem[0] + ' ' +elem[1] + ' ' + elem[2])
#    pandatest.columns[1:]
#    
#
##selected_columns = pandatest.columns[0:len(pandatest.columns)-2]
#
#
#datalog_values=pandatest.values[:,0:len(newlabels)]
##datalog_values[:,0:len(newlabels)]
#
#
#daylog_df_test= pd.DataFrame(datalog_values,
#                        index=pandatest.index,
#                        columns=newlabels)
#  
#print(daylog_df_test.head(5))
#

##plot all the channels with battery voltage:
#chanel_number = [i for i, elem in enumerate(newlabels) if 'Ubat' in elem]
#fig100=plt.figure(100)
#
#daylog_df.plot(y=daylog_df.columns[chanel_number],figsize=(15,5))
#plt.title('All Battery Voltages', fontsize=16, weight="bold")
#plt.ylabel('Voltage [V]', fontsize=12)
#plt.grid(True)


#plot manually the channels with battery voltage:
#
#fig10=plt.figure(10)
#plt.clf()
#plt.plot(daylog_df.index, daylog_df.values[:,13], 'b')
#plt.plot(daylog_df.index, daylog_df.values[:,35], 'g')
#plt.plot(daylog_df.index, daylog_df.values[:,0], 'r')
#
#plt.xlabel('Time (days)', fontsize=12)
#plt.ylabel('Voltage [V]', fontsize=12)
#plt.title('Battery Voltage', fontsize=18, weight="bold")
#plt.grid(True)
#
#fig10.legend(['mesure XT', 'mesure BSP', 'xt min'])
#plt.show()




#df.plot(subplots=True, figsize=(15,6))
#df.plot(y=["R", "F10.7"], figsize=(15,4))
#df.plot(x="R", y=["F10.7", "Dst"], style='.')
#



#***************************************
# task 2: Read and load results of the first .csv file
#****************************************
if filename[0:2]=='nx':
    offsetcolumn=0
else:
    offsetcolumn=1
        
#day_datalog=xt_log_day_import(file_path, user_delimiter)
daylog_df=xt_daylog_pandas_import(file_path, user_delimiter,offsetcolumn)


#set that first element in the list of all days (if ther are many)
#all_datalogs=[day_datalog]
all_datalogs_df=[daylog_df]
#all_datalogs_df.append(daylog_df)

new_time = time.time()
print("--- %s seconds ---" % (new_time - old_time))
old_time=new_time
print(" \n ")



#%***************************************
#% task 3: Check if they are other days after this one in the same folder (.csv file)
#%****************************************
#%start from the selected file date:
last_cvs_filename_used=filename;


year_string=['08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25']  #until 2025 is enough for now...
       
month_string=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    
day_string=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
number_of_files=1    
for year in year_string:
    for month in month_string:
        for day in day_string:
            cvs_filename=headfilename+year+ month+ day+'.CSV' 
            cvs_path=folder_path+'/'+cvs_filename
            
            #one more test to take only newer files than the one selected:
            first_file_date=str(year_f)+ str(month_f) +str(day_f)
            test_date=year+ month+ day
            
            if int(test_date)>int(first_file_date):   
                file_exist=True
                try:
                    f = open(cvs_path)
                    f.close()
                except IOError:
                    #print('File ', cvs_filename, ' is not accessible')
                    file_exist=False
                    
                if file_exist is True:
                    #print('File ', cvs_path, ' is accessible')
                    print('File ', cvs_filename, ' is accessible')
                    #day_datalog=xt_log_day_import(cvs_path, user_delimiter)
                    try:
                        daylog_df2=xt_daylog_pandas_import(cvs_path, user_delimiter,offsetcolumn)
                        
                        #Add that day to the other datalogs in the list of datalogs
                        #all_datalogs.append(day_datalog)
                        all_datalogs_df.append(daylog_df2)
                        number_of_files+=1
                    except:
                        print(' \n XXXXXXXXX PROBLEM with File ', cvs_filename, '     XXXXXXXXX    \n ')



#%***************************************
#% task 4: Concatenate those datas in one array
#%****************************************
#Concatenate those data
                    
print(" \n__________ Concatenate data  _______________ ")

#total_time_vectors=np.array([])
#total_datalog_value=np.array([])
#
#number_of_files=0
#for single_days in all_datalogs:
#    if number_of_files==0:
#        total_time_vectors= single_days['time_minutes_of_the_day']
#        total_datalog_value=single_days['datalog_value']
#    else:
#        total_time_vectors=np.append(total_time_vectors, single_days['time_minutes_of_the_day']+1440*number_of_files)
#        total_datalog_value=np.vstack((total_datalog_value, single_days['datalog_value']))
#    
#    number_of_files+=1   
#    
             
total_datalog_df=pd.concat(all_datalogs_df)  #concatenate all the daily dataFrames imported in a single one





#***************************************
# task 5: Cleaning of data
#****************************************      
#there are often holes in the datas, with 0 instead of real datas
#not so important for most of the values but for battery levels it is not OK
#replace it with the value of the minute before.


print(" ")
print(" __________ Warning: CLEAN OF DATA FOR BATTERIES  _______________ ")

channels_labels=list(total_datalog_df.columns)

#scan for channels with Ubat in the name:
matching2 = [i for i, elem in enumerate(channels_labels) if 'XT-Ubat' in elem]

#REPLACE 0 values with previous value
for chan in matching2:
    k=0
    for tested_value in total_datalog_df.values[:,chan]:
        if tested_value<1.0:
            total_datalog_df.values[k,chan]=total_datalog_df.values[k-1,chan]
            print("Error in batt voltage ")
        k+=1   
            


print(" ")
print(" __________ Warning: CLEAN OF DATA FOR TRANSFERT RELAY_______________ ")
#REPLACE 2 values (undetermined) with 0.5 to estimate the transfert time
#if there were a switch over during this minute, lets consider the transfer was like previously...

chanel_number_for_transfer=[i for i, elem in enumerate(channels_labels) if 'XT-Transfert' in elem]
k=0
for tested_value in total_datalog_df.values[:,chanel_number_for_transfer]:
    if tested_value>1.5:
        total_datalog_df.values[k,chanel_number_for_transfer]=total_datalog_df.values[k-1,chanel_number_for_transfer]
        print("Transfer transition ")
    k+=1   
            
    


#print(" ")
#print(" __________ Warning: CLEAN OF ... TODO _______________ ")
#



#%***************************************
#% task 6: resemple: day, month, year and put them in new dataframes
#%****************************************
    
quarters_mean_df=total_datalog_df.resample("15T",label='right').mean()
day_mean_df=total_datalog_df.resample("1d").mean()
month_mean_df=total_datalog_df.resample("1M").mean()
year_mean_df=total_datalog_df.resample("1Y").mean()

#change the names to distinguish (per example on graphs)
newlabels_q=[]
newlabels_d=[]
newlabels_M=[]
newlabels_Y=[]

k=0
for elem in list(total_datalog_df.columns):
    newlabels_q.append('15min mean ' + elem)
    newlabels_d.append('Day mean ' + elem)
    newlabels_M.append('Month mean ' + elem)
    newlabels_Y.append('Year mean ' + elem)
    k=k+1
    
quarters_mean_df.columns=newlabels_q  
day_mean_df.columns=newlabels_d     
month_mean_df.columns=newlabels_M    
year_mean_df.columns=newlabels_Y   
    
    



#***************************************
#Save in file the precomputed datas for later for the graph display
#***************************************

file_name='saved_dataframe_log_min'
total_datalog_df.to_pickle(file_name) 
file_name='saved_dataframe_log_quarters'
quarters_mean_df.to_pickle(file_name) 



#total_datalog_df = pd.read_pickle(file_name)
file_name='saved_dataframe_log_day'
day_mean_df.to_pickle(file_name) 
file_name='saved_dataframe_log_month'
month_mean_df.to_pickle(file_name) 
file_name='saved_dataframe_log_year'
year_mean_df.to_pickle(file_name) 


#import matplotlib.pyplot as plt
#import pandas as pd
#file_name='saved_dataframe_log_min'
#total_datalog_df = pd.read_pickle(file_name)
#file_name='saved_dataframe_log_quarters'
#quarters_mean_df=pd.read_pickle(file_name) 
#file_name='saved_dataframe_log_day'
#day_mean_df = pd.read_pickle(file_name)
#file_name='saved_dataframe_log_month'
#month_mean_df = pd.read_pickle(file_name)
#file_name='saved_dataframe_log_year'
#year_mean_df = pd.read_pickle(file_name)
#
#



#%***************************************
#% task 6: compute kWh
# WARNING: it make sense only for P in KW
#TODO: make a dataframe for energies
#%****************************************

#min to day: *60*24/1000
#day to month: *60*24/1000

day_kwh_df=total_datalog_df.resample("1d").sum()/60
month_kwh_df=total_datalog_df.resample("1M").sum()/60
year_kWh_df=total_datalog_df.resample("1Y").sum()/60

    




#***************************************
#%Timer
#***************************************

new_time = time.time()
print("--- %s seconds ---" % (new_time - old_time))
old_time=new_time


print("--TOTAL TIME- %s seconds ---" % (new_time - start_time))

    
print(" ")
print(" __________ GRAPH DISPLAY  _______________ ")
print(" \n \n \n ")





channels_labels=list(total_datalog_df.columns)


################################
#plot all the channels with battery voltage and current:
chanels_number_ubat = [i for i, elem in enumerate(channels_labels) if 'Ubat' in elem]
chanels_number_ibat = [i for i, elem in enumerate(channels_labels) if 'Ibat' in elem]

#fig_bat=plt.figure()
#fig_batt, axes_bat = plt.subplots(nrows=2, ncols=1)


total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_ubat],
                      grid=True,
                      figsize=(15,5),
                      sharex=True)

plt.ylabel('Voltage [V]', fontsize=12)
plt.title('All Battery Voltages', fontsize=12, weight="bold")
plt.grid(True)
plt.show


total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_ibat],
                      figsize=(15,5),
                      grid=True,
                      sharex=True)

plt.ylabel('Amperes [A]', fontsize=12)
plt.title('All Battery Currents', fontsize=12, weight="bold")
plt.grid(True)
plt.show





month_mean_df.plot(y=month_mean_df.columns[chanels_number_ubat[0]],
                      color='r',
                      figsize=(15,5),
                      grid=True,
                      sharex=True,
                      title='Mean Battery Voltages')





#
#
#
#
#
#######################################
##plot all the channels with Power 
#chanels_number_Pout = [i for i, elem in enumerate(channels_labels) if 'Pout' in elem]
##fig100=plt.figure(100)
#fig_pow, axes_pow = plt.subplots(nrows=1, ncols=2)
#
#total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_Pout],
#                      figsize=(12,6),
#                      ax=axes_pow[0],
#                      grid=True)
#
#plt.ylabel('Power activ/reactiv [kW/kVA]', fontsize=12)
#plt.title('All AC-out Powers', fontsize=12, weight="bold")
#
#
#
#
#total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_Pout[0]],
#                      marker='+',
#                      figsize=(12,6),
#                      ax=axes_pow[1])
#quarters_mean_df.plot(y=quarters_mean_df.columns[chanels_number_Pout[0]],
#                      marker='o',
#                      ax=axes_pow[1])
##plt.ylabel('Power activ/reactiv [kW/kVA]', fontsize=12)
#plt.title('1min and 15min AC-out Power', fontsize=12, weight="bold")
#plt.grid(True)
#
#
#
#
#
#fig_hist, axes_hist = plt.subplots()
#quarters_mean_df.plot(y=quarters_mean_df.columns[chanels_number_Pout[0]],
#                      figsize=(12,6),
#                      kind='hist',
#                      bins=20,
#                      ax=axes_hist)
#
#plt.title('Histogramm of Powers', fontsize=12, weight="bold")
#plt.xlabel('Power', fontsize=12)
#
#plt.grid(True)
#
#
##total_datalog_df.hist(y=total_datalog_df.values[:,chanels_number_Pout],
##                      bins=10,
##                      ax=axes2[1])
##
##quarters_mean_df.plot(quarters_mean_df.values[:,chanels_number_Pout],
##                      bins=20)
##
##plt.title('All AC-out Powers Histogram', fontsize=12, weight="bold")
##plt.grid(True)
##plt.xlabel('Power [kW]', fontsize=12)
#
#plt.show()
#
#
#
#
#######
## Charge /discharge power
########
#
#chanel_number_for_UbattBSP=[i for i, elem in enumerate(channels_labels) if 'BSP-Ubat [Vdc]' in elem]
#chanel_number_for_IbattBSP=[i for i, elem in enumerate(channels_labels) if 'BSP-Ibat [Adc]' in elem]
#
#
#battery_power=total_datalog_df.values[:,chanel_number_for_UbattBSP]*total_datalog_df.values[:,chanel_number_for_IbattBSP]/1000
#
##battery_power_df=pd.DataFrame({"Battery Power [kW]": battery_power,
##                               "Battery Charge Power [kW]": battery_power,
##                               "Battery Discharge Power [kW]": battery_power},
##                                index=total_datalog_df.index)
#               
#
#
#
#
#
#######################
## Battery analysis 
#######
#chanels_number_ubatbsp = [i for i, elem in enumerate(channels_labels) if 'BSP-Ubat' in elem]
#chanels_number_ibatbsp = [i for i, elem in enumerate(channels_labels) if 'BSP-Ibat' in elem]
#
#
#plt.plot(total_datalog_df.values[:,chanels_number_ubatbsp],total_datalog_df.values[:,chanels_number_ibatbsp])
#
#plt.ylabel('Amperes [A]', fontsize=12)
#plt.xlabel('Voltage [V]', fontsize=12)
#plt.title('Voltage VS Currents', fontsize=12, weight="bold")
#plt.grid(True)
#plt.show
#
#
#
##Temps en transfert:
#chanel_number_for_transfer=[i for i, elem in enumerate(channels_labels) if 'XT-Transfert' in elem]
#minutes_without_transfer=np.count_nonzero(total_datalog_df.values[:,chanel_number_for_transfer] == 0.0) 
#minutes_with_transfer=np.count_nonzero(total_datalog_df.values[:,chanel_number_for_transfer] == 1.0)
# 
#len(total_datalog_df.values[:,chanel_number_for_transfer])
#
#labels = ['on grid/genset: ' +str(round(minutes_with_transfer/60,1)) + ' hours',
#          'on inverter: ' +str(round(minutes_without_transfer/60,1)) + ' hours']
#fig_transfer=plt.figure()
#plt.clf()
#plt.pie([minutes_with_transfer,minutes_without_transfer],
#        labels=labels,
#        shadow=True, 
#        startangle=90,
#        autopct='%1.1f%%')
#        
#plt.show()
#
#
#
##Analyse Batterie
##
##fig = plt.figure()
##ax = plt.subplot(111)
##df1['Col1'].plot(ax=ax)
##df2['Col2'].plot(ax=ax)
#
#fig_batt_anlys, axes_batt_anlys = plt.subplots(nrows=1, 
#                           ncols=1,
#                           figsize=(15,5))
##axes4_2 = axes4.twinx()
#
#total_datalog_df.plot(y=total_datalog_df.columns[chanels_number_ubat],
#                      figsize=(15,5),
#                      grid=True,
#                      title='All Battery Voltages',
#                      ax=axes_batt_anlys)
#
#month_mean_df.plot(y=month_mean_df.columns[chanels_number_ubat[1]],
#                      color='r',
#                      ax=axes_batt_anlys)
#
#plt.ylabel('Voltage [V]', fontsize=12)
#plt.title('All Battery Voltages', fontsize=12, weight="bold")
#plt.grid(True)
#
##axes4.bar(x=month_mean_df.index, 
##        y=total_datalog_df.columns[chanels_number_ubat],
##        color='r',
##        ax=axes4_2)
##
##axes4.plot(x=total_datalog_df.index,
##         y=total_datalog_df.columns[chanels_number_ubat],
##         grid=True,
##         title='All Battery Voltages',
##         ax=axes4)
#
#
#
#
#
##Energies Mensuelles:
#
##month_kwh_df['XT-Pout a [kW] I3101 L1-1']
#fig_ener, axes_ener = plt.subplots(nrows=1, 
#                           ncols=1,
#                           figsize=(15,5))
#
#
#
#
##month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(grid=True,
##                      kind='line',
##                      marker='o',
##                      color='red',
##                      ax=axes_ener)
#
#month_kwh_df[['Solar power (ALL) [kW] I17999 ALL','XT-Pin a [kW] I3119 L1-1','XT-Pout a [kW] I3101 L1-1']].plot.bar(grid=True,
#                      stacked=False,
#                      ax=axes_ener)
#
#plt.ylabel('Energy [kWh]', fontsize=12)
#plt.title('Energies Mensuelles', fontsize=12, weight="bold")
#plt.grid(True)
#
#plt.show()
#
#
#fig_ener2, axes_ener2 = plt.subplots(nrows=1, 
#                           ncols=1,
#                           figsize=(9,9))
#
#
#
#month_kwh_df[['Solar power (ALL) [kW] I17999 ALL','XT-Pin a [kW] I3119 L1-1']].plot.bar(stacked=True,
#                      ax=axes_ener2,
#                      use_index=False,
#                      align='edge',
#                      width=0.5)
#
#
#month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(kind='bar',
#                      color='red',
#                      align='center',
#                      width=0.5,
#                      ax=axes_ener2,
#                      use_index=False)
#
#month_kwh_df['XT-Pout a [kW] I3101 L1-1'].plot(kind='line',
#                      marker='o',
#                      color='red',
#                      ax=axes_ener2,
#                      use_index=False)
#
#
#plt.ylabel('Energy [kWh]', fontsize=12)
#
##replace labels with the month name:
#loc, label= plt.xticks()
#plt.xticks(loc,labels=list(month_kwh_df.index.month_name()) )
#
#plt.title('Energies Mensuelles', fontsize=12, weight="bold")
#plt.grid(True)
#
#
#
#
#
#
########
### HEAT MAPS:  TODO
#########
##https://scipython.com/book/chapter-7-matplotlib/examples/a-heatmap-of-boston-temperatures/
##https://vietle.info/post/calendarheatmap-python/
#
#
#
#
#
##
########
### Charge /discharge power
#########
##
##chanel_number_for_UbattBSP=[i for i, elem in enumerate(channels_labels) if 'BSP-Ubat [Vdc]' in elem]
##chanel_number_for_IbattBSP=[i for i, elem in enumerate(channels_labels) if 'BSP-Ibat [Adc]' in elem]
##
##
##battery_power=total_datalog_df.values[:,chanel_number_for_UbattBSP]*total_datalog_df.values[:,chanel_number_for_IbattBSP]/1000
#
##battery_power_df=pd.DataFrame({"Battery Power [kW]": battery_power,
##                               "Battery Charge Power [kW]": battery_power,
##                               "Battery Discharge Power [kW]": battery_power},
##                                index=total_datalog_df.index)
##                               
##                               
#
#
##t = np.arange(0.0, 2, 0.01)
##s1 = np.sin(2*np.pi*t)
##s2 = 1.2*np.sin(4*np.pi*t)
##
##
##fig, ax = plt.subplots(20)
##ax.set_title('using span_where')
##ax.plot(t, s1, color='black')
##ax.axhline(0, color='black', lw=2)
##
##collection = collections.BrokenBarHCollection.span_where(
##    t, ymin=0, ymax=1, where=s1 > 0, facecolor='green', alpha=0.5)
##ax.add_collection(collection)
##
##collection = collections.BrokenBarHCollection.span_where(
##    t, ymin=-1, ymax=0, where=s1 < 0, facecolor='red', alpha=0.5)
##ax.add_collection(collection)
##
##
##plt.show()
#
#
#
#
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
#fig3=plt.figure(3)
#plt.clf()
#plt.plot(minutes_of_the_day/60, grid_power, 'b')
#
#
#plt.xlabel('Time (hours)', fontsize=12)
#plt.ylabel('Power [kW]', fontsize=12)
#plt.title('Grid Power', fontsize=18, weight="bold")
#
#plt.ax = fig3.gca()
#plt.ax.grid(True)
#
#plt.show()
#
#
#fig4=plt.figure(4)
#plt.clf()
#plt.plot(minutes_of_the_day/60, BSP_I_batt_val, 'b')
#
#
#plt.xlabel('Time (hours)', fontsize=12)
#plt.ylabel('I [A dc]', fontsize=12)
#plt.title('Battery Current', fontsize=18, weight="bold")
#
#plt.ax = fig4.gca()
#plt.ax.grid(True)
#
#

#fig1.legend(['mesure XT', 'mesure BSP', 'xt min'])



##pour un essai de vitesse d'affichage on stack 2^11 fois la journée, soit 2048 jours, soit 5,6 ans
#
#batt_val_long=batt_val
#for k in range(11):
#    batt_val_long=np.append(batt_val_long,batt_val_long)
#    
#    
#fig3=plt.figure(3)
#plt.clf()
#plt.plot(batt_val_long, 'r+-')
#
#plt.xlabel('Voltage')
#plt.ylabel('Occurence')
#plt.title('Histogram of Battery Voltage')
#plt.text(52, 25, r'$\mu=100,\ \sigma=15$')
##plt.axis([40, 60, 0, 0.03])
#plt.grid(True)
#plt.show()
#
#plt.ax = fig3.gca()
#plt.ax.grid(True)
