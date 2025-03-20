#!/bin/bash
CURRENT_PATH="$(pwd)"

FILEPATH_SERVERS="$CURRENT_PATH/servers.json" # This file is .json because it is a consult to an endpoint
FILEPATH_OUTPUT="$CURRENT_PATH/servers.csv"
LIST_DATA=()
IFS=,
spinner=("Formatting data... -" "Formatting data... \\" "Formatting data... |" "Formatting data... /")

######################### BEGIN 1 ###############################

if [ ! -f $FILEPATH_SERVERS ]; then
    curl "$DEVICES" > "$FILEPATH_SERVERS"
fi


######################### END 1 ################################
# Load Spinner
spinner() {
    while :; do
        for i in "${spinner[@]}"; do
            echo -ne "\r$i"
            sleep 0.1
        done
    done
}

# Delete other version of response data snmp
if [ -f $FILEPATH_OUTPUT ]; then
    rm -r $FILEPATH_OUTPUT
fi

# If the script is run manually, the load spinner will come up.
if [ -n "$USERNAME" ]; then 
    spinner &
    spinner_pid=$!
fi

# Start time registration
echo "Time started: $(date)"

######################### BEGIN 2 ##############################

if [ -f $FILEPATH_SERVERS ]; then
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
    done < "$FILEPATH_SERVERS"

    total=${#LIST_DATA[@]}
    for (( i = 0; i < $total; i+=2)); do
        j=$(( i + 1 ))
        echo "${LIST_DATA[$i]},${LIST_DATA[$j]}" >> "$FILEPATH_OUTPUT"
    done

    total_register=$(cat $FILEPATH_OUTPUT | wc -l)
else 
    echo "Data of all servers not found."
fi

######################### END 2 ##############################
# If the script is run manually, the load spinner will come down.
if [ -n "$USERNAME" ]; then 
    kill $spinner_pid
    wait $spinner_pid
fi
# End time registration
echo -e "\nTime finished: $(date)"
echo "Total of registered servers: $total_register"