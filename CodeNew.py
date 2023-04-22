# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:55:22 2023

@author: laqm
"""

import pyvisa


import pyvisa
import csv
import time
from lakeshore import Model335
from lakeshore.model_335 import *
import numpy as np
import logging as log
import pandas as pd

#to manually change which device/method, uncomment change this checker variable
#0 for delta mode, 1 for lock-in, 2 for pulse delta
#checker = 0

rm = pyvisa.ResourceManager()
global starttime 
starttime1 = time.time()
starttime2 = time.time()

if 'GPIB0::16::INSTR' in rm.list_resources():
    my_instrument = rm.open_resource('GPIB0::16::INSTR')
    checker = 0
    #6221 is connected
else:
    my_instrument = rm.open_resource('GPIB0::8::INSTR')
    checker = 1
    #lock-in amplifier is connected
    
my_model_335 = Model335(57600)


#create global variables for inputting values
global L
global P
global I
global D
global rampenable
global rampvalue
global setpointin

def getparameters():
    
    L = 1
    P = 50
    I = 20
    D = 0
    rampenable = False
    rampvalue = 0
    setpointin = 10
    
    my_model_335.set_heater_pid(1, P, I, D)
    my_model_335.set_control_setpoint(1, setpointin)
    my_model_335.set_setpoint_ramp_parameter(1, rampenable, rampvalue)
    
    

def autosensitivity(channel1x):
    
    sensitivityold = {0: "2 nV/fA",		13: "50 uV/pA",
                    1: "5 nV/fA",		14: "100 uV/pA",
                    2: "10 nV/fA",	    15: "200 uV/p                                                                                                                                    ",
                    3: "20 nV/fA",	    16: "500 uV/pA",
                    4: "50 nV/fA",	    17: "1 mV/nA",
                    5: "100 nV/fA",	    18: "2 mV/nA",
                    6: "200 nV/fA",	    19: "5 mV/nA",
                    7: "500 nV/fA",	    20: "10 mV/nA",
                    8: "1 uV/pA",		21: "20 mV/nA",
                    9: "2 uV/pA",		22: "50 mV/nA",
                    10: "5 uV/pA",		23: "100 mV/nA",
                    11: "10 uV/pA",	    24: "200 mV/nA",
                    12: "20 uV/pA",	    25: "500 mV/nA",
                    26: "1 V/uA"}
    
    newvalue = 10*(channel1x)


    sensitivity = [(2*10**-9), 5*10**-9, (1*10**-8), 2*10**-8, 5*10**-8, 1*10**-7, 2*10**-7, 5*10**-7, 
                   1*10**-6, 2*10**6, 5*10**-6, 1*10**-15, 2*10**-15, 5*10**-15, 1*10**-15, 2*10**-15, 5*10**-15,
                   1*10**-3, 2*10**-3, 5*10**-3, 1*10**-2, 2*10**-2, 5*10**-2, 1*10**-1, 2*10**-1, 5*10**-1]

    xmax = []
    count = 0
    for x in sensitivity:
            i = (newvalue - x)
            
            if(i >= 0):
                xmax.append(i)
            else:
                xmax.append(500)
       
    minimumindex = xmax.index(min(xmax))
    #print(minimumindex)
    #print(sensitivity[minimumindex])
    return minimumindex     
      
               
def gettemperature():
    
    value = my_model_335.get_kelvin_reading(1)
    return value
    
def getPID():
    return my_model_335.get_heater_pid(1)

def ramprate():
    return my_model_335.get_setpoint_ramp_parameter(1)

    return my_model_335.get_control_setpoint(1)



#variable for sensitivity entry into CSV file
sensitivityold = {0: "2 nV/fA",		13: "50 uV/pA",
                1: "5 nV/fA",		14: "100 uV/pA",
                2: "10 nV/fA",	    15: "200 uV/pA",
                3: "20 nV/fA",	    16: "500 uV/pA",
                4: "50 nV/fA",	    17: "1 mV/nA",
                5: "100 nV/fA",	    18: "2 mV/nA",
                6: "200 nV/fA",	    19: "5 mV/nA",
                7: "500 nV/fA",	    20: "10 mV/nA",
                8: "1 uV/pA",		21: "20 mV/nA",
                9: "2 uV/pA",		22: "50 mV/nA",
                10: "5 uV/pA",		23: "100 mV/nA",
                11: "10 uV/pA",	    24: "200 mV/nA",
                12: "20 uV/pA",	    25: "500 mV/nA",
                26: "1 V/uA"}



#-----------------START OF CODE-----------------------------------------------------------------------------------------



#my_model_335.get_all_kelvin_reading()

# create initial rows in file
def create_file():
    with open('3-25-lock-in-test.csv', mode='w', newline="") as csv_file:
    
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        if checker == 1:
            writer.writerow(['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)', 'Sensitivity', 'Temperature', 'PID', 'Ramprate', 'Setpoint'])
        if checker == 0:
            writer.writerow(['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)', 'Sensitivity', 'Temperature', 'PID', 'Ramprate', 'SetPoint'])


#begin data collection 
def data_collect():

    global my_model_335
   
        
    if checker == 1:
            
            count = 0
            voltageincrement = 0.1
            timevalue = 0
            starttime = 0
            endtime = 0
            
            while count < 86400:
            #run for 1.9 seconds
                
                
                channel1 = my_instrument.query_ascii_values("OUTP? {}".format(1))[0]
                #index1 = autosensitivity(channel1)
                #my_instrument.write("SENS {}".format(index1))
                #sensitivity = sensitivityold[index1]
                
                #new sensitivity 
                #sensitivity = my_instrument.query_ascii_values("SENS? {}".format(1))[0]
                sensitivity = 1
                
                channel1 = my_instrument.query_ascii_values("OUTP? {}".format(1))[0] 
                freq = my_instrument.query_ascii_values('FREQ?')[0]
                voltage = my_instrument.query_ascii_values('SLVL?')[0]
                channel2 = my_instrument.query_ascii_values("OUTP? {}".format(2))[0] 
             
                temperature1 = gettemperature()
                PID = getPID()
                ramprate1 = ramprate()
                setpointA = my_model_335.get_control_setpoint(1)
    
                
                values = [timevalue, voltage, freq, channel1, channel2, sensitivity, temperature1, PID, ramprate1, setpointA]
                
                # create initial rows in file
                with open('3-28-lock-in-test.csv', mode='a', newline="") as csv_file:
                
                    writer = csv.writer(csv_file, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(values)
            
            
                count = count + 2
                time.sleep(2)
                timevalue = timevalue + 2
                timevalue = round(timevalue, 2)
                voltageincrement = voltageincrement + 0.3
                #my_instrument.write("SLVL {}".format(voltageincrement))
                
                
    if checker == 2:   
        timevalue = 0

        x = 0
        keithleyarray = []

        my_instrument.write('*RST') #restores 6221 defaults
        my_instrument.write("TRAC:CLE") 

        my_instrument.write('SYST:COMM:SER:SEND "REN"')

        #setup2182A
        voltrange = 0.01 
        log.info("Setting up 2182A measurement range and integration rate")
        my_instrument.write('SYST:COMM:SER:SEND "VOLT:RANG %f"' % voltrange) #sets 2V range for 2182a
        log.info("Voltage range has been set to %f V" % voltrange)

        rate = 1
        my_instrument.write('SYST:COMM:SER:SEND "VOLT:NPLC %f"' % rate) #Set rate to 1PLC for 2182a
        #my_instrument.query('SYST:COMM:SER:SEND "VOLT:NPLC?"') #send rate query
        #my_instrument.query('SYST:COMM:SER:SEND: "ENT?"') #return response to query
        log.info("VIntegration rate has been set to %f V" % rate)
            

        #setup6221Delta
        log.info("Beginning sequence to set up, arm, and run Delta")
        my_instrument.write('*RST') #restores 6221 defaults
        my_instrument.write('SOUR:PDEL:HIGH 1e-6') #sets high source value 
        #my_instrument.write('SOUR:PDEL:LOW -10e-6') #sets low source value 
        my_instrument.write("SOUR:PDEL:SDEL 9.16e-4") #sets delta delay 
        my_instrument.write("SOUR:PDEL:WIDT 4.16e-3") #sets width 
        my_instrument.write('SOUR:PDEL:COUN 1') #Sets Delta count 
        #my_instrument.write('SOUR:DELT:CAB ON') #Enables compliance abort
        my_instrument.write('TRAC:POIN 1')#sets buffer 
        log.info('Set up completed')
        my_instrument.write('SOUR:PDEL:ARM') #Arms Delta
        #armed = my_instrument.query('SOUR:DELT:ARM?') #queries if armed
        #armed = 1
        
        print('current is ' + my_instrument.query('SOUR:PDEL:HIGH?'))
        with open('3-30keithleypulse.csv', mode='w', newline="") as csv_file:

            writer = csv.writer(csv_file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(['Time', 'Readings', 'Temperature','setpoint'])

        while (x < 1000000000):
            
            time1 = time.time()
         
            
            #up to here it is 0.015 seconds
            
            #measuring
            my_instrument.write('INIT:IMM') #starts delta measurements
            log.info('Delta measurements have started')
            
            #readings
            my_instrument.query('SENS:DATA?')
            
            time.sleep(0.05)
            timevalue = timevalue + 0.05
            
            time2 = time.time()
            #print(time2-starttime)
            #up to here it is 1.82 seconds
            
            
            #Remove the extra characters from the output values 
            temp = str(my_instrument.query('TRAC:DATA?'))
            print('data '+ temp)
            var = temp.replace('+', '')
            print(var)
            var2 = var.split(',')[0]
            print(var2)
            #keithleyarray.append(var2)
            #print(keithleyarray)
            
            
            temperature1 = gettemperature()
            temporary = str(temperature1)
            x1 = temporary.replace('[', '')
            x2 = x1.replace(']', '')
            x3 = x2.replace('"', '')
            temperature1 = float(x3)
            PID = getPID()
            ramprate1 = ramprate()
            setpointA = my_model_335.get_control_setpoint(1)
            
            x = x + 0.1 
            end = time.time()
            #up to here it is 1.833 seconds
           
            values = [round(timevalue,2), var2, temperature1, setpointA]
            #print(values)
            #adding the time value increment to the time elapsed since code started
            with open('3-30keithleypulse.csv', mode = 'a', newline='') as f:
                writer = csv.writer(f, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                writer.writerow(values)
                
               
            
            
            #wait around 2 seconds between every measurement
            time.sleep(2)
            timevalue = timevalue + 2
            timevalue = round(timevalue, 2)
            

        #finished
        #time.sleep(10)

        #reset
        my_instrument.write('*RST') #restores 6221 defaults
        my_instrument.write("TRAC:CLE") 




    if checker == 0:
            
            timevalue = 0

            x = 0
            keithleyarray = []

            my_instrument.write('*RST') #restores 6221 defaults
            my_instrument.write("TRAC:CLE") 

            my_instrument.write('SYST:COMM:SER:SEND "REN"')

            #setup2182A
            voltrange = 0.01 
            log.info("Setting up 2182A measurement range and integration rate")
            my_instrument.write('SYST:COMM:SER:SEND "VOLT:RANG %f"' % voltrange) #sets 2V range for 2182a 
            
            log.info("Voltage range has been set to %f V" % voltrange)

            rate = 1
            my_instrument.write('SYST:COMM:SER:SEND "VOLT:NPLC %f"' % rate) #Set rate to 1PLC for 2182a
           
            log.info("VIntegration rate has been set to %f V" % rate)
                

            #setup6221Delta
            log.info("Beginning sequence to set up, arm, and run Delta")
            my_instrument.write('*RST') #restores 6221 defaults
            my_instrument.write('SOUR:DELT:HIGH 5e-6') #sets high source value 
            #my_instrument.write("SOUR:DELT:DEL 100e-3") #sets delta delay 
            my_instrument.write('SOUR:DELT:COUN 1') #Sets Delta count 
            
            #enable autorange feature
            my_instrument.write('SOUR:CURR:RANGE:AUTO 1')
            #print(my_instrument.query('SOUR:CURR:RANGE:AUTO?'))
            my_instrument.write('SOUR:CURR:RANGE:AUTO 1')

            
            #my_instrument.write('SOUR:DELT:CAB ON') #Enables compliance abort
            my_instrument.write('TRAC:POIN 1') #sets buffer 
            log.info('Set up completed')
            my_instrument.write('SOUR:DELT:ARM') #Arms Delta
            #armed = my_instrument.query('SOUR:DELT:ARM?') #queries if armed
            #armed = 1
            print('current is ' + my_instrument.query('SOUR:DELT:HIGH?'))

            with open('3-9-23-deltatest5microamps.csv', mode='w', newline="") as csv_file:

                writer = csv.writer(csv_file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)

                writer.writerow(['Time', 'Readings', 'Temperature', 'PID', 'RampRate', 'Setpoint'])

            while (x < 600000):
                
                time1 = time.time()
             
                
                #up to here it is 0.015 seconds
                
                #measuring
                my_instrument.write('INIT:IMM') #starts delta measurements
                log.info('Delta measurements have started')
                
                #readings
                my_instrument.query('SENS:DATA?')
                
                time2 = time.time()
                deltatime1 = time2-starttime1
                print(deltatime1)
                #up to here it is 1.82 seconds
                
                #time.sleep(0.05)
                #timevalue = timevalue + 0.05
                
                temp = str(my_instrument.query('TRAC:DATA?'))
                var = temp.replace('+', '')
                print(var)
                var2 = var.split(',')[0]
                print(var2)
                #keithleyarray.append(var2)
                #print(keithleyarray)
                
                x = x + 0.1 
                end = time.time()
                #up to here it is 1.833 seconds
                
                #removing brackets and quotes from temperature entry
                temperature1 = gettemperature()
                temporary = str(temperature1)
                x1 = temporary.replace('[', '')
                x2 = x1.replace(']', '')
                x3 = x2.replace('"', '')
                temperature1 = float(x3)
                PID = getPID()
                ramprate1 = ramprate()
                setpointA = my_model_335.get_control_setpoint(1)
                
                deltatime2 = end - starttime1
                values = [round(timevalue+(deltatime2),2), var2, temperature1, PID, ramprate1, setpointA]
               
                #adding the time value increment to the time elapsed since code started
                with open('3-9-23-deltatest5microamps.csv', mode = 'a', newline='') as f:
                    writer = csv.writer(f, delimiter=',',
                                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    
                    writer.writerow(values)
                    
                   
                
                
                
                time.sleep(1)
                timevalue = timevalue + 1
                timevalue = round(timevalue, 2)
                

            #finished
            #time.sleep(10)

            #reset
            my_instrument.write('*RST') #restores 6221 defaults
            my_instrument.write("TRAC:CLE") 


    
    my_model_335 = 0



# read
def read_file():
    with open(r'3-25-lock-in-test.csv', newline="") as csv_file:
        reader = csv.reader(csv_file)
     
        for item in reader:
          print(item)


getparameters()
if checker == 1:
    create_file()
data_collect()
if checker == 1:
    read_file()






#each iteration in the while loop takes 5.2 * 10^-6, so time taken to run loop is negigible
#can do user input of sampling rate and let choose whether every 0.5 seconds, 0.1 seconds, etc.
