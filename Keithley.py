#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:31:05 2022

This is an attempt to code a program to use Keithley 6221 and 2182A
to measure a resistor


@author: libby
"""


import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
import pymeasure
from pymeasure.log import console_log

import csv
import numpy as np
import time
import pandas as pd
import pyvisa as visa
import serial


rm = visa.ResourceManager('@py')
rm.list_resources()
#print(rm.list_resources())
my_instrument = rm.open_resource('GPIB0::16::INSTR')

print(my_instrument)


def first_step():
    rm = visa.ResourceManager('@py')
    rm.list_resources()
    #print(rm.list_resources())
    my_instrument = rm.open_resource('GPIB0::16::INSTR')

    print(my_instrument)

def connect():
    #my_instrument.write("*rst; status:preset; *cls")
    print(my_instrument.query('*IDN?'))
    log.info('Checking IDN to see if properly connected')
    my_instrument.write('*RST') #restores 6221 defaults
    my_instrument.write("TRAC:CLE") 
    #my_instrument.write('TRAC:FEED SENS1')

############################################################
###to talk to 2182A, must use SYST:COMM:SER:SEND "<data>"###
############################################################



def setup2182A():
    setup2complete = 0
    connection = int(my_instrument.query('SOUR:DELT:NVPR?')) #checks if connected to 2182a
    my_instrument.write('SYST:COMM:SER:SEND "REN"')
    if connection == 0:
        log.info('ERROR: No connection to 2182A')
    if connection == 1:
        voltrange = 0.01 
        log.info("Setting up 2182A measurement range and integration rate")
        my_instrument.write('SYST:COMM:SER:SEND "VOLT:RANG %f"' % voltrange) #sets 2V range for 2182a
        #my_instrument.query('SYST:COMM:SER:SEND "VOLT:RANG?"') #send range query
        #my_instrument.query('SYST:COMM:SER:SEND: "ENT?"') #return response to query
        log.info("Voltage range has been set to %f V" % voltrange)
    
        rate = 1
        my_instrument.write('SYST:COMM:SER:SEND "VOLT:NPLC %f"' % rate) #Set rate to 1PLC for 2182a
        #my_instrument.query('SYST:COMM:SER:SEND "VOLT:NPLC?"') #send rate query
        #my_instrument.query('SYST:COMM:SER:SEND: "ENT?"') #return response to query
        log.info("VIntegration rate has been set to %f V" % rate)
        setup2complete = 1
        return setup2complete
    
def setup6221Delta():
    setup6complete = 0
    connection = int(my_instrument.query('SOUR:DELT:NVPR?')) #checks if connected to 2182a
    if connection == 0:
        log.info('ERROR: No connection to 2182A')
    if connection == 1:
        log.info("Beginning sequence to set up, arm, and run Delta")
        my_instrument.write('*RST') #restores 6221 defaults
        my_instrument.write('SOUR:DELT:HIGH 1e-5') #sets high source value to 1mA
        my_instrument.write("SOUR:DELT:DEL 100e-3") #sets delta delay to 100 ms
        my_instrument.write('SOUR:DELT:COUN 65536') #Sets Delta count to 1000
        #my_instrument.write('SOUR:DELT:CAB ON') #Enables compliance abort
        my_instrument.write('TRAC:POIN 65536') #sets buffer to 1000 points
        log.info('Set up completed')
        my_instrument.write('SOUR:DELT:ARM') #Arms Delta
        armed = my_instrument.query('SOUR:DELT:ARM?') #queries if armed
        #armed = 1
        if armed == 0:
            log.info('ERROR: Not armed')
        if armed == 1:
            log.info('Delta armed')
            setup6complete = 1
        return setup6complete

def measuring():
    my_instrument.write('INIT:IMM') #starts delta measurements
    log.info('Delta measurements have started')

def readings():
    my_instrument.query('SENS:DATA?') #Reads latest delta reading
            
def finished(file_name):
    time.sleep(9000)
    log.info('No longer taking in data. Shutting down delta measuring and moving onto reading buffer')
    my_instrument.write("SOUR:SWE:ABOR") #Stops delta, disarms, and places 2182a in local mode
    log.info('Now reading the buffer')
    values = str(my_instrument.query('TRAC:DATA?'))
    split_values = values.split(",")
    time.sleep(10)
    log.info("Delta readings have been loaded onto an array")
    header = ['Readings', 'Time']
    data = np.reshape(split_values, (65536,2))
    with open(str(file_name) + '.csv', 'w', encoding = 'UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print('checkpoint 4')
    
    
def resetforDeltareadings():
    my_instrument.write('*RST') #restores 6221 defaults
    my_instrument.write("TRAC:CLE") 
    #my_instrument.write('TRAC:FEED SENS1')
    
    
    
if __name__ == "__main__":
    i=0
    while i<10:
        console_log(log)
        
        new_name = 'night_data_' + str(i)
        
        first_step()
    
        connect()
        setup2182A()
        setup6221Delta()
        measuring()
        readings()
        finished(new_name) 
        resetforDeltareadings()
        i+=1
    
    
    

    