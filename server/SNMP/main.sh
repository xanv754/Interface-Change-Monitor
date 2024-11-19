#!/bin/bash
spinner=("Getting consults SNMP... -" "Getting consults SNMP... \\" "Getting consults SNMP... |" "Getting consults SNMP... /")
current_date=$(date +%Y-%m-%d)
communities=()

FROM=$1
TO=$2
PART=$3
USERNAME=$(echo $USER)
CURRENTPATH="$(echo $HOME)/Interface-Change-Monitor/server/SNMP"
PING="$CURRENTPATH/ping.sh"
SNMP="$CURRENTPATH/consult.sh"
INPUT="$CURRENTPATH/devices.txt"
OUTPUT="$CURRENTPATH/data/SNMP_"$current_date"_part_$PART"

##########################################################
# Load Spinner
spinner() {
    while :; do
        for i in "${spinner[@]}"; do
            echo -ne "\r$i"
            sleep 0.1
        done
    done
}
#########################################################
# Check if the "FROM" and "TO" are correct values
if [ $TO -lt $FROM ]; then
    echo "Bad values of 'from' and 'to' input."
    exit 1
fi

# Check of the data file (devices)
if [ ! -f $INPUT ]; then
    echo "Data file not found."
    exit 1
fi

# Delete other version of consults SNMP with the same date
if [ -f $OUTPUT ]; then
    rm $OUTPUT
fi

# If the script is run manually, the load spinner will come up.
if [ -n "$USERNAME" ]; then 
    spinner &
    spinner_pid=$!
fi

# Check if this is the first consult
if [ $FROM != 0 ]; then
    FROM=$((FROM + 1))
fi
#############################################################
# Start time registration
echo "Time started: $(date)"

# Programm Begin
while IFS=, read -r col1 col2
do
    ip="$col1"
    community="$col2"
    communities+=("$ip")
    communities+=("$community")
done < "$INPUT"

consult_realized=0

for (( i = $FROM; consult_realized <= $TO; i+=2)); do
    j=$(( i + 1 ))
    ip=${communities[$i]}
    community=${communities[$j]}
    response=$(bash $PING $ip)
    if [ -n "$response" ]; then
        bash $SNMP $OUTPUT $community $ip $current_date
    fi
    consult_realized=$((consult_realized + 1))
done
# Programm End

# If the script is run manually, the load spinner will come down.
if [ -n "$USERNAME" ]; then 
    kill $spinner_pid
    wait $spinner_pid
fi

# End time registration
echo -e "\nTime finished: $(date)"