#!/bin/bash
CURRENTPATH=$(pwd)
FILEPATH="$CURRENTPATH/devices.json"

if [ -f $FILEPATH ]; then
    rm "$FILEPATH"
fi

curl "$DEVICES" > "$FILEPATH"