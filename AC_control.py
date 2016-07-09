#!/usr/bin/python3

#Code for controlling my air conditioner

print('This code controls my air-conditioner over infrared.')

import os
import sys
import time
import json
import serial

#define messages
messages = {}
messages['on'] = b'%\xff\xff\x01\xaa\xa8\xa8\x8a\xa8\x8a\xaa\x22\x8a\xaa\x02\x00'
messages['off'] = b'%\xff\xff\x01\x54\x51\x51\x15\x51\x45\x55\x15\x45\x55\x01\x00'

#check number of input arguments
if len(sys.argv) == 2:
   #check valid input argument
   if sys.argv[1] in messages:
       print('Executing Command: ' + sys.argv[1])
       print('By sending code:')
       print(messages[sys.argv[1]])
   else:
       print('Invalid Command')
       print('Valid Commands Are:')
       print(list(messages.keys()))
       #exit program
       exit()
else:
   print('Wrong Number of Input Arguments')
   print('Script Usage:')
   print('./AC_control.py <command>')
   #exit program
   exit()

#load previous serial settings or prompt for new ones
settings_file = '/home/pi/settings.json'
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

#open serial port
s = serial.Serial(serial_settings['port'],serial_settings['baud'],timeout=3)
print('Serial Port Connected.')

#opening serial resets arduino
#wait a few seconds for it to restart
print('Waiting for Arduino to restart...')
time.sleep(5)

#send command
s.write(messages[sys.argv[1]])
print('Command Sent.')

print('Verifying Command:')
#arduino echo's back the command
#read this and print to user
hold = 1
string = b'%'
while hold:
    ch = s.read(1)
    if ch == b'\n':
        hold = 0
    else:
        string += ch
print(string)

if string == messages[sys.argv[1]]:
    print('Command Verified')
else:
    print('Failed to Verify')

#close serial port
s.close()
print('Port Closed')
