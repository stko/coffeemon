#!/bin/bash
REDIR=$(/bin/grep -i redirURL $1 | /usr/bin/cut -d = -f 2)
NAME=$(/bin/grep -i name $1 | /usr/bin/cut -d = -f 2)
PASSWORD=$(/bin/grep -i password $1 | /usr/bin/cut -d = -f 2)
WSURL=$(/bin/grep -i wsurl $1 | /usr/bin/cut -d = -f 2)
PORT=$(/bin/grep -i port $1 | /usr/bin/cut -d = -f 2)


if [ -z "$REDIR" -o -z "$NAME" -o -z "$PASSWORD" ]; then
        exit 0
fi
if [ -z "$PORT"  ]; then
        PORT=80
fi
#MYIP=$(ifconfig eth0 | grep -i "inet " | cut -d ':' -f 2 | cut -d ' ' -f 1)
MYIP=$(/sbin/ifconfig eth0 | /bin/grep -i "inet " | /usr/bin/cut -d ' ' -f 10)

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
  /bin/echo "${encoded}"    # You can either set a return variable (FASTER) 
  REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p
}
### if your webservice runs on another server and/or port, uncomment and configure it here
#WSURL=ws://$MYIP:9000

WSURLENC=$( rawurlencode "$WSURL" )
### if your iot web server does not straigt under in the web root on port 80, configure it here
IOTURL=http://$MYIP:$PORT?wsurl=$WSURLENC

### set your device name & password here

IOTURLENC=$( rawurlencode "$IOTURL" )
# wait "loop" in case of service repeated restart if curl exists with an error
/bin/sleep 5
REDIRSERVER="$REDIR?name=$NAME&password=$PASSWORD&url=$IOTURLENC"
#curl --silent $REDIRSERVER > /dev/null
/bin/echo "$REDIRSERVER"
/usr/bin/curl  "$REDIRSERVER" 
exit $?
