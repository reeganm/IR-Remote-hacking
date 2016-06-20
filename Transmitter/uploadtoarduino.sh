#!/bin/sh

echo Congrads, you are too lazy to type avrdude command

avrdude -p m328p -P /dev/ttyACM0 -c arduino -b 115200 -F -u -U flash:w:$1

echo Laziness successful
