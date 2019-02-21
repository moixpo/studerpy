# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 20:33:51 2019

@author: moix_
"""

#reset of the workspace and close all existing figures
from IPython import get_ipython
get_ipython().magic('reset -sf') 


import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk
from tkinter import filedialog
import time

from studer_datalog_day_converter import studer_datalog_day_converter

#close all existing figures
plt.close("all")


#OPTIONS:
user_delimiter=';'  # ',' for english Excel display and ';' for french Excel option change in the RCC



#***************************************
# task 1: Choose the first .csv file
#****************************************

#the dialog window to select the first file to import:
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
file_path_split=file_path.split('/')
filename=file_path_split[len(file_path.split('/'))-1]
folder_path=file_path[:-12]

#path_name=file_path_split[0:len(file_path.split('/'))-1]
# format LG180402.CSV

year_f=filename[2:4]
month_f=filename[4:6]
day_f=filename[6:8]

print(file_path)


#timing to optimize the code:
start_time = old_time= time.time()




#***************************************
# task 2: Read and load results of the first .csv file
#****************************************

   
day_datalog=studer_datalog_day_converter(file_path, user_delimiter)

#set that first element in the list of all days (if ther are many)
all_datalogs=[day_datalog]

new_time = time.time()
print("--- %s seconds ---" % (new_time - old_time))
old_time=new_time
print(" \n ")



#%***************************************
#% task 3: Check if they are other days after this one in the same folder (.csv file)
#%****************************************
#%start from the selected file date:
last_cvs_filename_used=filename;


year_string=['07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']  #until 2022 is enough
       
month_string=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    
day_string=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32']
number_of_files=1    
for year in year_string:
    for month in month_string:
        for day in day_string:
            cvs_filename='LG'+year+ month+ day+'.CSV' 
            cvs_path=folder_path+cvs_filename
            
            #one more test to take only older files than the selected:
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
                    day_datalog=studer_datalog_day_converter(cvs_path, user_delimiter)
                    #Add that day to the other datalogs in the list of datalogs
                    all_datalogs.append(day_datalog)
                    number_of_files+=1
                


#%***************************************
#% task 4: Concatenate those datas in one array
#%****************************************
#Concatenate those 
total_time_vectors=np.array([])
total_datalog_value=np.array([])

number_of_files=0
for single_days in all_datalogs:
    if number_of_files==0:
        total_time_vectors= single_days['time_minutes_of_the_day']
        total_datalog_value=single_days['datalog_value']
    else:
        total_time_vectors=np.append(total_time_vectors, single_days['time_minutes_of_the_day']+1440*number_of_files)
        total_datalog_value=np.vstack((total_datalog_value, single_days['datalog_value']))
    
    number_of_files+=1   
    
             

#***************************************
# task 5: Cleaning of data
#****************************************      
#there are often holes in the datas, with 0 instead of real datas
#not so important for most of the values but for battery levels it is not OK


print(" __________ Warning: CHECK CHANNELS FOR BATTERIES  _______________ ")

chanel_number_for_batteries=[0, 1, 2, 39, 40, 41]  #TODO: scan for channels with Ubat in the name 

#REPLACE 0 values
for chan in chanel_number_for_batteries:
    k=0
    for tested_value in total_datalog_value[:,chan]:
        if tested_value<1.0:
            total_datalog_value[k,chan]=total_datalog_value[k-1,chan]
        k+=1   
            
    
print(" __________ Warning: CHECK CHANNELS FOR TRANSFERT RELAY  _______________ ")
chanel_number_for_batteries=[0, 1, 2, 39, 40, 41]
    
    
#REPLACE 2 values (undetermined) with 0.5 to estimate the transfert time

# TODO

    
    
    
    
    
    
print(" ")
print(" __________ GRAPH DISPLAY  _______________ ")
print(" \n \n \n ")

chanel_number=0
batt_valmin=total_datalog_value[:,chanel_number]
chanel_number=39
batt_val=total_datalog_value[:,chanel_number]

minutes_of_the_day=total_time_vectors




fig1=plt.figure(1)
plt.clf()
plt.plot(minutes_of_the_day/60, total_datalog_value[:,chanel_number], 'b')
plt.plot(minutes_of_the_day/60, total_datalog_value[:,chanel_number+1], 'c')
plt.plot(minutes_of_the_day/60, total_datalog_value[:,chanel_number+2], 'g')


plt.plot(minutes_of_the_day/60, batt_valmin,'y+-')

plt.xlabel('Time (hours)', fontsize=12)
plt.ylabel('Voltage', fontsize=12)
plt.title('Battery Voltage', fontsize=18, weight="bold")

plt.ax = fig1.gca()
plt.ax.grid(True)

plt.show()



fig2=plt.figure(2)
plt.clf()
plt.hist(batt_val, 25, facecolor='r', alpha=0.75)

plt.xlabel('Voltage')
plt.ylabel('Occurence')
plt.title('Histogram of Battery Voltage')
plt.text(52, 25, r'$\mu=100,\ \sigma=15$')
#plt.axis([40, 60, 0, 0.03])
plt.grid(True)
plt.show()

plt.ax = fig2.gca()
plt.ax.grid(True)


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

plt.show()


new_time = time.time()
print("--- %s seconds ---" % (new_time - old_time))
old_time=new_time


print("--TOTAL TIME- %s seconds ---" % (new_time - start_time))