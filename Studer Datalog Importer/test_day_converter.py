###################################
#studer_datalog_day_converter.py
#  Version py 1.0   3 février 2019
#  Moix P-O
#  OFFGRID.CH   Albedo-Engineering ALBEDO.CH
######################
#
#studer_datalog_day_converter(filename, user_delimiter=',')
#
##   filename: name of the log file: LG091006.CSV per example
##
##   user_delimiter=','      for english Excel display used by default 
##   user_delimiter=';'      for french Excel
##
##
##
##The returned DAY_DATALOG is a structure with the following fields
##
##day_datalog =
##             channels_label: {1xn cell}           Name of the n channels logged
##                        day: 6                     Day of the month
##                      month: 10                    month of the year
##                       year: 2009                  year
##    time_minutes_of_the_day: [1x1440 double]       time in minutes of the logged day
##              datalog_value: [n x1440x9 double]    n channels 
#
#


#%reset y
#%timeit

#https://janakiev.com/blog/csv-in-python/

#import scipy
#from scipy import *
#from scipy.optimize import differential_evolution

import matplotlib.pyplot as plt
import numpy as np
#import panda
import csv


import tkinter as tk
from tkinter import filedialog
import time


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



#studer_datalog_day_converter(file_path,',')

#def studer_datalog_day_converter(filename, user_delimiter=','):
    
other_infos=[]
with open(file_path) as csv_file:
    
    csv_reader = csv.reader(csv_file, delimiter=user_delimiter)
    line_count = 0
    values_line_count = 0
    
    #initialisation à vide des vecteurs dans lesquels les données seront stockées:
    #datalog_value_list=[]
    #date_list=[]
    #datalog_value_array=np.array([])
    
    #month=np.array([])
    #batt_val=np.array([])
    minutes_of_the_day=np.array([])
    
    
    
    for row in csv_reader:
        #print(row)
        
        if line_count == 0:
            #print(f'Column names are:  \n {", ".join(row)} \n')
            version_datalog=row[0]
            channels_names=row[1:len(row)]
            
            
        elif line_count == 1:
            #print(f'Info param num are: \n{", ".join(row)} \n')
            infos_user_names=row[1:len(row)]
            
        elif line_count == 2:
            phases_names=row[1:len(row)]
            #print(f'Phases are: \n {", ".join(row)} \n')
            
        elif line_count>1442:
            other_infos=other_infos+row
            #print(row)
            # A organiser mieux si on veut en tirer des infos de ce qui est à la fin des log
            
            
        else:
            time_character=row[0]
            #Then we have to convert this time given as: day.month.year hh.mm
            # 01.01.2009 00:00
            # 01.01.2009 00:01
            # 01.01.2009 00:02
            
                      
            #sort les heures et les minutes de la 
            time_of_day=time_character.split(' ')[1]
            

            
            hh=int(time_of_day.split(':')[0])
            mm=int(time_of_day.split(':')[1])
            
            minutes_of_the_day=np.append(minutes_of_the_day, [mm+60*hh], axis=0)
            #print( 'jour: ', d_o_m, ' de l annee ' , year , 'minute: ' , minutes_of_the_day[values_line_count])
            
            
            #mise en vecteur des données:
            datalog_value_raw=list(row[1:len(row)]) #le resultat est une liste avec  les données en string
            
            #convertit en float et remplit les trous manquants par des 0.0:
            datalog_value_float=[(float(x) if x else 0.0) for x in datalog_value_raw]
            
            
            #conversion en un array de nombres:
            datalog_value_line = np.array(datalog_value_float)
            #n.astype(np.float)
            #si c'est le premier passage crée l'array de base pour ajouter les autres après (sinon problème de taille avec les stack) 
            
            if values_line_count==0:
                datalog_value_array=datalog_value_line
            else:                   
                #if hole in the data: copy line before:
                if len(datalog_value_line)<2:
                    datalog_value_array= np.vstack((datalog_value_array,datalog_value_array[values_line_count-1,:]))
                else:
                    datalog_value_array= np.vstack((datalog_value_array,datalog_value_line))
                             
                    
            values_line_count += 1
            
            
        line_count += 1
        
        
        
    #print(f'Processed {line_count} lines.')


#print("NOMBRE DE LIGNES= ", values_line_count , " ET DE COLONNES: ", len(channels_names)+1)



#sort le jour, le mois et l'annee de la date (pas besoin dans la boucle)
date=time_character.split(' ')[0]

d_o_m=int(date.split('.')[0])
month=int(date.split('.')[1])
year=int(date.split('.')[2]) 
            
# retraitement des données importée
day_of_month=np.ones(len(minutes_of_the_day))*d_o_m



#Construit la sortie: on met tout dans une structure (dictionnaire en python) 

day_datalog={'channels_label': channels_names, 'day':d_o_m, 'month': month, 'year':year , 'time_minutes_of_the_day':minutes_of_the_day, 'datalog_value': datalog_value_array, 'version_datalog':version_datalog, 'other_infos':other_infos}
##day_datalog =
##             channels_label: {1xn cell}           Name of the n channels logged
##                        day: 6                     Day of the month
##                      month: 10                    month of the year
##                       year: 2009                  year
##    time_minutes_of_the_day: [1x1440 double]       time in minutes of the logged day
##              datalog_value: [n x1440x9 double]    n channels 
##             version_datalog:'v6.10'
   





print(" ")
print(" ______________  DISPLAY  ______________________________ ")
print(" \n \n \n ")

chanel_number=0
batt_valmin=day_datalog['datalog_value'][:,chanel_number]
chanel_number=39
batt_val=day_datalog['datalog_value'][:,chanel_number]


batt_val_long=batt_val

##pour un essai de vitesse d'affichage on stack 2^11 fois la journée, soit 2048 jours, soit 5,6 ans
#for k in range(11):
#    batt_val_long=np.append(batt_val_long,batt_val_long)

fig1=plt.figure(1)
plt.clf()
plt.plot(minutes_of_the_day/60, batt_val, 'b+-')
plt.plot(minutes_of_the_day/60, batt_valmin,'y+-')

plt.xlabel('Time (hours)')
plt.ylabel('Voltage')
plt.title('Battery Voltage')

plt.ax = fig1.gca()
plt.ax.grid(True)

plt.show()
