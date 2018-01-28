#!/bin/sh
# CAUTION: IOTURL and WSRURL need to be given as uerlencoded Strings! To convert them easily,
# use some of the online coding tools like https://www.url-encode-decode.com/
IOTURL=http%3A%2F%2Flocalhost%3A8080%2F%3Fwsurl%3Dws%253A%252F%252Flocalhost%253A9000
NAME=cm1
PASSWORD=passwort
REDIRSERVER="http://localhost:8080/redirect.php?name=$NAME&password=$PASSWORD&url=$IOTURL"
#curl --silent $REDIRSERVER > /dev/null
echo $REDIRSERVER
curl  $REDIRSERVER 
