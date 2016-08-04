#!/usr/bin/python3

#Code for controlling my air conditioner

print('This code logs temperature from my Arduino and puts it on a firebase server')

path = '/home/pi/IR-Remote-hacking/'
myDataBase = 'https://mydatabase-f7de1.firebaseio.com/'

import os
import sys
import time
import json
import serial
import datetime
from firebase import firebase

#load previous serial settings or prompt for new ones
settings_file = path + 'settings.json'
if os.path.isfile(settings_file):
    #read file
    f = open(settings_file,'r')
    serial_settings = json.load(f)
    f.close()
    print('Detected Previous Port Settings')
else:
    print('Can not detect port settings')
    print('Prompting User:')
    serial_settings = {'port':0,'baud':0}
    serial_settings['port'] = input('What port?: ')
    serial_settings['baud'] = input('What Baudrate?: ')
    #save settings file
    f = open(settings_file,'w')
    json.dump(serial_settings,f, indent=4)
    f.close()

valid_chars = [ord('0'), ord('1'),ord('2'),ord('3'),ord('4'),ord('5'),ord('6'),ord('7'),ord('8'),ord('9'),ord('.'),ord('-'), ord('\n')]
def readlineCR(port):
    #wait for start of line %
    hold = 1
    while hold:
        ch = port.read(1)
        ch = ord(ch)
        if ch == ord('%'):
            hold = 0
    rv = ""
    while True:
        ch = port.read(1)
        ch = ord(ch)
        if ch in valid_chars:
            rv += chr(ch)
            if ch==ord('\n'): #if there is a new line
                 print(rv)
                 return(rv)

#open serial port
try:
   s = serial.Serial(serial_settings['port'],serial_settings['baud'],timeout=3)
except:
   print('error with serial settings')
   os.remove(settings_file)
   sys.exit(3)
   
print('Serial Port Connected.')

#opening serial resets arduino
#wait a few seconds for it to restart
print('Waiting for Arduino to restart...')
time.sleep(5)

#send command
s.write(b'$')
print('Sending Temperature Request')

#read temperature
temp = readlineCR(s)

#remove \n
temp = temp[0:(len(temp)-1)]

#close serial port
s.close()
print('Port Closed')

#connect to firebase
print("Connecting to Firebase")
firebase = firebase.FirebaseApplication(myDataBase,None)

firebase.put('IR/temp',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),json.dumps({'TEMP':temp}))

print('Data written to firebase')

sys.exit(0)
