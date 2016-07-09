#!/usr/bin/python3

#sends off command to IR transmitter

import os
import json
import serial

#load previous serial settings are prompt for new ones
settings_file = 'settings.json'
if os.path.isfile(settings_file):
    #read file
    f = open(settings_file,'r')
    serial_settings = json.load(f)
    f.close()
else:
    serial_settings = {'port':0,'baud':0}
    serial_settings['port'] = input('What port?: ')
    serial_settings['baud'] = input('What Baudrate?: ')
    #save settings file
    f = open(settings_file,'w')
    json.dump(serial_settings,f, indent=4)
    f.close()


s = serial.Serial(serial_settings['port'],serial_settings['baud'])


off = b'%\xff\xff\x01\x54\x51\x51\x15\x51\x45\x55\x15\x45\x55\x01\x00'

s.write(off)

hold = 1
string = ''
while hold:
    ch = ord(s.read(1))
    ch = hex(ch)
    if ch == hex(ord('\n')):
        hold = 0
    else:
        print(ch)
s.close()
