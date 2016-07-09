#!/usr/bin/python3

import serial
import numpy as np
#import matplotlib.pyplot as plt
import time
import json
import sys
import os
import os.path


sample_rate = 33 #u_seconds

#### Serial Settings ####

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

valid_chars = [ord('0'), ord('1'), ord('\n')] #binary data

#### Reading Serial ####

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

try:
    #open serial
    s = serial.Serial(serial_settings['port'], baudrate=serial_settings['baud'])
    print('Serial Open')
    #receive string from arduino
    string = readlineCR(s)
    #close serial
    s.close()
except:
    #close serial
    s.close()
    print('serial connection problem')
    #exit program
    exit()

#### Data Processing ####

#remove \n
string = string[0:(len(string)-1)]

#split characters
bits = list(string)

#convert to integers
bits = [ int(x) for x in bits ]

num_samples = len(bits)

#find length of each "bit"
a = np.array([], dtype=int)
hold  = bits[0]
c = 0
for m in bits:
    if m == 0:
        if hold == 0:
            c += -1 #count 0 as negative
        if hold == 1:
            hold = 0
            a = np.append(a,[c])
            c = -1
    else:
        if hold == 1:
            c += 1 #count 1 as positive
        if hold == 0:
            hold = 1
            a = np.append(a,[c])
            c = 1
a = np.append(a,[c])

#find length of single bit (shortest "bit" is a single bit)
bit_length = np.min(np.abs(a))
#reduce
a = a / bit_length
#numpy rounds 0.5's to the nearest even number
a = np.rint(a) 

#build reduced data byte
d = np.array([], dtype=int)
for n in a:
    if n < 0:
        d = np.hstack((d,np.zeros(int(np.abs(n)),dtype=int)))
    else:
        d = np.hstack((d,np.ones(int(np.abs(n)),dtype=int)))

bits2 = d.tolist()

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

#bit time
bit_time = bit_length*sample_rate
#this will always under estimate bit time :(
#to do: better frequency calculation

print('Bit time: ',bit_time)
print('Code: ',d)

#plt.plot( list(range(0,num_samples*sample_rate,sample_rate)) , bits, list(range(0,len(bits2)*bit_time,bit_time)), bits2)
#plt.axis([0,num_samples*sample_rate,0,1.5])
#plt.show()


