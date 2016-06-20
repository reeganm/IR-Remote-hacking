!#/usr/bin/sh

ssh pi@$1 -p $2 "sudo dmesg|grep tty"
