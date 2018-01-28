#!/bin/bash
MYIP=$(ifconfig eth0 | grep -i "inet ad" | cut -d ':' -f 2 | cut -d ' ' -f 1)

# automated url encoding thanks to https://stackoverflow.com/a/10660730
rawurlencode() {
  local string="${1}"
  local strlen=${#string}
  local encoded=""
  local pos c o

  for (( pos=0 ; pos<strlen ; pos++ )); do
     c=${string:$pos:1}
     case "$c" in
        [-_.~a-zA-Z0-9] ) o="${c}" ;;
        * )               printf -v o '%%%02x' "'$c"
     esac
     encoded+="${o}"
  done
  echo "${encoded}"    # You can either set a return variable (FASTER) 
  REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p
}
### if your webservice runs on another server and/or port, uncomment and configure it here
#WSURL=ws://$MYIP:9000

WSURLENC=$( rawurlencode "$WSURL" )
### if your iot web server does not straigt under in the web root on port 80, configure it here
IOTURL=http://$MYIP?wsurl=$WSURLENC

### set your device name & password here
NAME=cm1
PASSWORD=passwort


IOTURLENC=$( rawurlencode "$IOTURL" )


REDIRSERVER="http://localhost:8080/redirect.php?name=$NAME&password=$PASSWORD&url=$IOTURLENC"
#curl --silent $REDIRSERVER > /dev/null
echo $REDIRSERVER
curl  $REDIRSERVER 
