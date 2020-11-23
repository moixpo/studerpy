# Read user info 3001, Battery temperature, (Modbus register 2) from the first Xtender
# Run this example within the 'examples/' folder using 'python ex_read_info.py' from a CLI after installing
#   xcom485i package with 'pip install xcom485i'
#import matplotlib.pyplot as plt
import serial
import time

from xcom485i.client import Xcom485i

SERIAL_PORT_NAME = 'COM3'  # your serial port interface name
SERIAL_PORT_BAUDRATE = 9600  # baudrate used by your serial interface
DIP_SWITCHES_ADDRESS_OFFSET = 0  # your modbus address offset as set inside the Xcom485i device


#A few registers named: see Technical specification Studer Modbus RTU Appendix V1.6.20.pdf

BATTERY_REGISTER_XT_TO_READ=0 # Battery Voltage on Xtender
TEMPERATURE_REGISTER_TO_READ=2 # Battery Temperature BTS
STATE_OF_CHARGE_REGISTER=14 # 
STATE_OF_XT=98 # XT is ON or OFF
STATE_OF_REMOTE_ENTRY_XT= 172

BATTERY_REGISTER_VARIO_TO_READ=0 # Battery Voltage on Variotrack
PV_VOLT_REGISTER_VARIO_TO_READ=4 # Battery Voltage on Variotrack

    

if __name__ == "__main__":
    try:
        serial_port = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUDRATE, parity=serial.PARITY_EVEN, timeout=1)
    except serial.serialutil.SerialException as e:
        print("\n Check your serial configuration : ", e)
    else:
        #xcom485i = Xcom485i(serial_port, DIP_SWITCHES_ADDRESS_OFFSET, debug=True)
        xcom485i = Xcom485i(serial_port, DIP_SWITCHES_ADDRESS_OFFSET, debug=False)
        
        
        read_value = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, BATTERY_REGISTER_XT_TO_READ)
        #print('read_value:', read_value)
        print(' ')
        print('Battery Voltage On Xtender:', read_value, 'Volts')
        battery_volt_mes=read_value
        
        read_value = xcom485i.read_info(xcom485i.addresses.vt_1_device_id, BATTERY_REGISTER_VARIO_TO_READ)
        #print('read_value:', read_value)
        print(' ')
        print('Battery Voltage On Variotrack:', read_value, 'Volts')
        battery_volt_mes=read_value
        
        read_value = xcom485i.read_info(xcom485i.addresses.vt_1_device_id, PV_VOLT_REGISTER_VARIO_TO_READ)
        #print('read_value:', read_value)
        print(' ')
        print('Photovoltaic Voltage On Variotrack:', read_value, 'Volts')
        battery_volt_mes=read_value   
        PV_VOLT_REGISTER_VARIO_TO_READ

    
        read_value = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, TEMPERATURE_REGISTER_TO_READ)
        #print('read_value:', read_value)
        print(' ')
        print('BTS Temperature:', read_value, '°C')
        bts_temp_mes=read_value

        
        read_value = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, STATE_OF_CHARGE_REGISTER)
        #print('read_value:', read_value)
        print(' ')
        if read_value ==32767.0:
            print('No SOC info in the XT, there is no BSP')
        else:
            print('SOC:', read_value, '%')
        soc_mes=read_value

        
        
        read_value = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, STATE_OF_XT)
        #print('read_value:', read_value)
        print(' ')
        #print('State of XT:', read_value)
        if read_value ==0.0:
            print('The Xtender is OFF')
        else:
            print('The Xtender is ON')
        
        
        read_value = xcom485i.read_info(xcom485i.addresses.xt_1_device_id, STATE_OF_REMOTE_ENTRY_XT)
        #print('read_value:', read_value)
        print(' ')
        #print('State of XT:', read_value)
        if read_value ==0.0:
            print('The Remote entry is 0')
        else:
            print('The Remote entry is activated')
        
        
#        #scan for xt_ ? _device_id
#        try:
#            read_value = xcom485i.read_info(xcom485i.addresses.xt_2_device_id, STATE_OF_XT)
#        except:
#            print("\n device 2 is not connected")
#        else:
#            print("\n device 2 is connected")
                        

    serial_port.close()
    