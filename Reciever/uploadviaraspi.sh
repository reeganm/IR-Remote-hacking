!#/usr/bin/sh

echo "This script loads hex file on to raspberry pi via ssh then uploads it to an 
arduino"

echo "Usage: ./uploadviaraspi.sh <hex_file> <arduino port> <ip address> <ssh-port>"

sftp -oPort=$4 pi@$3 <<< $"put $1"

ssh pi@$3 -p $4 "avrdude -p m328p -P $2 -c arduino -b 115200 -F -u -U flash:w:$1"

