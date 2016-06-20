!#/bin/sh

sftp -oPort=222 pi@reeganhome.ddns.net <<< $"put $1"

