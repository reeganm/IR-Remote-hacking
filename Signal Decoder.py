#!/usr/bin/python

import serial
import numpy as np
import time
import json
import sys
import os
import os.path

#load previous serial settings are prompt for new ones
settings_file = 'settings.json'
if os.path.isfile(settings_file):
    #read file
    f = open(settings_file,'r')
    Serial_Settings = json.load(f)
    f.close()
else:
    serial_settings = {'port':0,'baud':0}
    serial_settings['port'] = input('What port?: ')
    serial_settings['baud'] = input('What Baudrate?: ')
    #save settings file
    f = open(settings_file,'w')
    json.dump(serial_settings,f, indent=4)
    f.close()

valid_chars = ['0' '1' '\n']

def readlineCR(port):
    rv = b""
    while True:
        ch = port.read()
        if ch in valid_chars:
            rv += ch
            if ch=='\n': #if there is a new line
                 try:
                     #if it is a valid string it will decode
                     rv = rv.decode("utf-8")
                     print(rv)
                     return(rv)
                 except:
                     print("invalid string")
                     rv = b"" #start over
        else:
            print("invalid character received")

#try:
#s = serial.Serial(port, baudrate=baud, timeout=3.0)

#receive string from arduino
#string = readlineCR(port)
string = "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000000111111111100000000001111111111\n"
#remove \n
string = string[0:(len(string)-1)]
#split characters
bits = list(string)
#convert to integers
bits = [ int(x) for x in bits ]

#find length of each bit
a = np.array([], dtype=int)
hold  = bits[0]
c = 0
for m in bits:
    if m == 0:
        if hold == 0:
            c += -1
        if hold == 1:
            hold = 0
            a = np.append(a,[c])
            c = -1
    else:
        if hold == 1:
            c += 1
        if hold == 0:
            hold = 1
            a = np.append(a,[c])
            c = 1
a = np.append(a,[c])
#reduce
a = a / np.min(np.abs(a))
#numpy rounds 0.5's to the nearest even number
#this might cause issues
a = np.rint(a) 

#build reduced data byte
d = np.array([], dtype=int)
for n in a:
    if n < 0:
        d = np.hstack((d,np.zeros(int(np.abs(n)),dtype=int)))
    else:
        d = np.hstack((d,np.ones(int(np.abs(n)),dtype=int)))

#convert to bytes
numbytes = int(np.ceil(len(d)/8))
#add zeros to make an even number of bytes
while len(d) < numbytes*8:
    d = np.append(d,[0])

d = d.reshape((numbytes,8),order='C')

#flip order so LSb's are on right
d = np.fliplr(d)

#convert to list
d = d.tolist()

#convert to strings of bytes
#this is a lot harder than it should be
for k,row in enumerate(d):
    for j,col in enumerate(row):
        d[k][j] = str(d[k][j])
for index,row in enumerate(d):
    d[index] = ''.join(row)

#convert binary to decimal number
for b,bite in enumerate(d):
    bite = '0b' + bite
    d[b] = int(bite,2)

#convert to hex
for b,bite in enumerate(d):
    d[b] = hex(bite)

print(d)

#except:
    #print("something went wrong")
