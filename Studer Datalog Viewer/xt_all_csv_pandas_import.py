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
#REPLACE 2 values (undetermined) to estimate the transfert time
#if there were a switch over during this minute, lets consider the transfer was like previously...

chanel_number_for_transfer=[i for i, elem in enumerate(channels_labels) if 'XT-Transfert' in elem]
k=0
for tested_value in total_datalog_df.values[:,chanel_number_for_transfer]:
    if tested_value>1.5:
        total_datalog_df.values[k,chanel_number_for_transfer]=total_datalog_df.values[k-1,chanel_number_for_transfer]
        print("Transfer transition ")
    k+=1   
            
    


#print(" ")
#print(" __________ Warning: CLEAN OF ... other things to clean?? we'll see TODO _______________ ")
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
                      figsize=(15,8),
                      grid=True,
                      sharex=True,
                      ax=axes_bat_i)

axes_bat_i.set_ylabel('Amperes [A]', fontsize=12)
axes_bat_i.set_title('All Battery Currents', fontsize=12, weight="bold")
axes_bat_i.grid(True)


#
#
#
#month_mean_df.plot(y=month_mean_df.columns[chanels_number_ubat[0]],
#                      color='r',
#                      figsize=(15,5),
#                      grid=True,
#                      sharex=True,
#                      title='Mean Battery Voltages')



print(" ")
print(" *******  run xt_graph_plotter_pandas.py for detailled graphs  ****** ")
print(" \n \n \n ")
