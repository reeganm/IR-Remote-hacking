#!/usr/bin/python3

#sends on command to transmitter

import serial
import time
import json
import os

on = b'00%\xff\xff\x01\xaa\xa8\xa8\x8a\xa8\x8a\xaa\x22\x8a\xaa\x02\x00' #padded with starting 0's

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


s = serial.Serial(serial_settings['port'],serial_settings['baud'],timeout=3)


time.sleep(5)

s.write(on)

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
