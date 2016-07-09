#!/usr/bin/python3

#sends on command to transmitter

import serial

on = b'%\xff\xff\x01\xaa\xa8\xa8\x8a\xa8\x8a\xaa\x22\x8a\xaa\x02\x00'

s = serial.Serial('/dev/ttyACM0',9600)
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
