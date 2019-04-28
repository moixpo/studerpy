"""
###################################
#  xt_log_day_import.py
#  Version py 1.0   25 février 2019
#  Moix P-O
#  WWW.OFFGRID.CH   Albedo-Engineering ALBEDO.CH
#  License GPL-3.0-only ou GPL-3.0-or-later
######################



import serial

ser = serial.Serial('/dev/ttyUSB0')  # open serial port
ser.baudrate = 38400
ser.bytesize=8
ser.parity='N'


ser.open()

print('Damn! All the programming job is to do ...   ')


## First test will be sending the test frame given on page 27 of manual 
#AA
#00
#01 00 00 00
#65 00 00 00
#0A 00
#6F 71
#02
#01
#01 00
#B8 0B 00 00
#01 00
#00 C0 45 41
#C5 90



ser.close()


