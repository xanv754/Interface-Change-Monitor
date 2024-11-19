#!/bin/bash

CURRENTPATH=$(pwd)
INPUT="$CURRENTPATH/devices.json"
OUTPUT="$CURRENTPATH/devices.csv"
LIST_DATA=()
IFS=,
spinner=("Formatting IPs and communities... -" "Formatting IPs and communities... \\" "Formatting IPs and communities... |" "Formatting IPs and communities... /")

spinner() {
    while :; do
        for i in "${spinner[@]}"; do
            echo -ne "\r$i"
            sleep 0.1
        done
    done
}

if [ -f $INPUT ]; then
    spinner &
    spinner_pid=$!

    # BEGIN
    if [ -f $OUTPUT ]; then
        rm "$OUTPUT"
    fi

    while IFS= read -r line; do
        if [[ "$line" == *"\"ip\":"* ]]; then 
            ip=$(echo "$line" | cut -d ':' -f 2)
            ip="${ip//[,\"[:space:]]/}"
            LIST_DATA+=("$ip")
        elif [[ "$line" == *"\"community\":"* ]]; then 
            community=$(echo "$line" | cut -d ':' -f 2)
            community="${community//[,\"[:space:]]/}"
            LIST_DATA+=("$community")
        fi
    done < "$INPUT"

    total=${#LIST_DATA[@]}
    for (( i = 0; i < $total; i+=2)); do
        j=$(( i + 1 ))
        echo "${LIST_DATA[$i]},${LIST_DATA[$j]}" >> "$OUTPUT"
    done
    # END

    kill $spinner_pid
    wait $spinner_pid
else 
    echo "Data file not found."
fi