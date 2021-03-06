#!/usr/bin/python3

#Code for controlling my air conditioner

print('This code controls my air-conditioner over infrared.')

path = '/home/pi/IR-Remote-hacking/'

import os
import sys
import time
import json
import serial

#import messages
from IR_messages import messages

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
       #exit program with non zero
       sys.exit(1)
else:
   print('Wrong Number of Input Arguments')
   print('Script Usage:')
   print('./AC_control.py <command>')
   #exit program
   sys.exit(2)

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

sys.exit(0)
