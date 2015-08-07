#!/usr/bin/bash

HOST=$1
COUNT=${2-2000}
TIMEOUT=300
PROJECT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}")/../ && pwd)
CHANNEL_ID=foo
SALT=common

if [ -z $HOST ]; then
    echo "Host is required" >&2
    exit 1
fi

if [[ $HOST != http* ]]; then
    echo "Host is invalid. Should start with 'http'" >&2
    exit 1
fi

curl -vX POST $HOST/channels/new -d id=$CHANNEL_ID\&salt=$SALT &> /dev/null
echo "Channel path: $HOST/c/$CHANNEL_ID"

ws_path="$(echo $HOST | sed 's/^http/ws/g')/channels/$CHANNEL_ID"

timeout $TIMEOUT $PROJECT_DIR/node_modules/thor/bin/thor \
    --amount $COUNT \
    --messages=1000 \
    --generator $PROJECT_DIR/tests/load-generator.js \
    $ws_path
