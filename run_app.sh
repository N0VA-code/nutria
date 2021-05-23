#!/bin/bash -e

APP_ADDR="127.0.0.1"
APP_PORT="5000"

if [[ $(uname) == "Linux" ]]; then
    DIR=$(dirname $(readlink -f $0))
else
    echo "[!] set DIR variable manually"
    exit # DIR="path"
fi

exec $DIR/es/bin/elasticsearch -d
espid=$!
exec python $DIR/nutria/nutria.py --listen-port $APP_PORT --listen-addr $APP_ADDR 2> /dev/null > /dev/null &
pypid=$!

echo ''
echo "[+] starting the service at http://$APP_ADDR:$APP_PORT/"
echo ''

read -p "[-] If you want to quit, just press [q + enter] : " input
if [[ "$input" = "q" || "$input" = "Q" ]]; then
    echo '[+] gonna be quit'
    kill -9 $pypid
    kill -9 $espid
fi
