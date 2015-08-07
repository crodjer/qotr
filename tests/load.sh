#!/usr/bin/bash

HOST=$1
COUNT=${2-2000}
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

curl -sX POST $HOST/channels/new -d id=$CHANNEL_ID\&salt=$SALT
echo "\n" # QOTR's response doesn't add a newline.
echo "Channel path: $HOST/c/$CHANNEL_ID"

ws_path="$(echo $HOST | sed 's/^http/ws/g')/channels/$CHANNEL_ID"
thor=$PROJECT_DIR/node_modules/thor/bin/thor

$thor \
    --amount $COUNT \
    --messages=1000 \
    --generator $PROJECT_DIR/tests/load-generator.js \
    $ws_path
