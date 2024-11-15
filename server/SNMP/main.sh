#!/bin/bash
spinner=("Getting consults SNMP... -" "Getting consults SNMP... \\" "Getting consults SNMP... |" "Getting consults SNMP... /")
current_date=$(date +%Y-%m-%d)
communities=()

CURRENTPATH="$(pwd)/Interface-Change-Monitor/server/SNMP"
PING="$CURRENTPATH/ping.sh"
SNMP="$CURRENTPATH/consult.sh"
INPUT="$CURRENTPATH/devices.csv"
OUTPUT="$CURRENTPATH/data/SNMP_$current_date"

spinner() {
    while :; do
        for i in "${spinner[@]}"; do
            echo -ne "\r$i"
            sleep 0.1
        done
    done
}

echo "Time started: $(date)"

if [ ! -f $INPUT ]; then
    echo "Data file not found."
    exit 1
fi

if [ -f $OUTPUT ]; then
    rm $OUTPUT
fi

spinner &
spinner_pid=$!

# BEGIN
while IFS=, read -r col1 col2
do
    ip="$col1"
    community="$col2"
    communities+=("$ip")
    communities+=("$community")
done < "$INPUT"

total_communities=${#communities[@]}

for (( i = 0; i < $total_communities; i+=2)); do
    j=$(( i + 1 ))
    ip=${communities[$i]}
    community=${communities[$j]}
    response=$(bash $PING $ip)
    if [ -n "$response" ]; then
        bash $SNMP $OUTPUT $community $ip $current_date
    fi
done
# END

kill $spinner_pid
wait $spinner_pid
echo "Time finished: $(date)"