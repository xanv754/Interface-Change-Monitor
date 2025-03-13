#!/bin/bash
DIVISOR=$1
PARTITION=$2
NUMBER=$3

USERNAME=$(echo $USER)
CURRENT_DATE=$(date +%Y-%m-%d)
CURRENT_PATH="$(echo $HOME)/Interface-Change-Monitor/server/SNMP"
LOG="$(echo $HOME)/Interface-Change-Monitor/server/system.log"

DATA_SERVERS=()
spinner=("Getting consults SNMP... -" "Getting consults SNMP... \\" "Getting consults SNMP... |" "Getting consults SNMP... /")

SCRIPT_PING="$CURRENT_PATH/ping.sh"
SCRIPT_SNMP="$CURRENT_PATH/snmp.sh"

FOLDER_RESPONSE_SNMP="$CURRENT_PATH/data/$CURRENT_DATE"
FOLDER_TMP="$CURRENT_PATH/tmp"

FILE_DATA_SERVERS="$CURRENT_PATH/servers.csv"
FILE_DATA_SERVER_TMP="$FOLDER_TMP/server"$NUMBER".csv"

##########################################################
# Start time registration
echo "$(date +"%Y-%m-%d %H:%M:%S") INFO[/SNMP/main.sh] Start consults SNMP of today" >> $LOG

# Load Spinner
spinner() {
    while :; do
        for i in "${spinner[@]}"; do
            echo -ne "\r$i"
            sleep 0.1
        done
    done
}

# If the script is run manually, the load spinner will come up.
if [ -n "$USERNAME" ]; then 
    spinner &
    spinner_pid=$!
fi

# Delete other version of response data snmp
if [ -d $FOLDER_RESPONSE_SNMP ]; then
    rm -r $FOLDER_RESPONSE_SNMP
fi

# Delete folder tmp
if [ -d $FOLDER_TMP ]; then
    rm -r $FOLDER_TMP
fi

#################### BEGIN ##############################
# Check exists the data (ip's and communities)
if [ ! -f $FILE_DATA_SERVERS ]; then
    echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/main.sh] Data of all servers not found" >> $LOG
    if [ -n "$USERNAME" ]; then 
        kill $spinner_pid
        wait $spinner_pid
    fi
    echo "$(date +"%Y-%m-%d %H:%M:%S") INFO[/SNMP/main.sh] End consults SNMP of today" >> $LOG
    exit 1
fi

mkdir $FOLDER_TMP
mkdir $FOLDER_RESPONSE_SNMP

total_lines=$(cat $FILE_DATA_SERVERS | wc -l)
is_odd=$(( $total_lines % $DIVISOR ))

if [ $is_odd -eq 0 ]; then
    if [ $PARTITION -eq 1 ]; then
        start_line=1
        end_line=$((( $total_lines / $DIVISOR ) * $PARTITION))
    else 
        start_line=$((( $total_lines / $DIVISOR ) * ( $PARTITION - 1 )))
        start_line=$(( $start_line + 1 ))
        end_line=$((( $total_lines / $DIVISOR ) * $PARTITION ))
    fi
else 
    if [ $PARTITION -eq 1 ]; then
        start_line=1
        end_line=$((( $total_lines / $DIVISOR ) * $PARTITION))
    else 
        start_line=$((( $total_lines / $DIVISOR ) * ( $PARTITION - 1 )))
        start_line=$(( $start_line + 1 ))
        if [ $PARTITION -eq $DIVISOR ]; then
            end_line=$total_lines
        else 
            end_line=$((( $total_lines / $DIVISOR ) * $PARTITION ))
        fi
    fi  
fi

current_line=1
sed "1,$(($start_line-1))d" "$FILE_DATA_SERVERS" > $FILE_DATA_SERVER_TMP

while IFS=, read -r line; do
    ip=$(echo "$line" | awk -F ',' '{print $1}')
    community=$(echo "$line" | awk -F ',' '{print $2}')
    DATA_SERVERS+=("$ip")
    DATA_SERVERS+=("$community")
    if [ $current_line -ge $end_line ]; then
        break
    fi
    current_line=$(( $current_line + 1 ))
done < "$FILE_DATA_SERVER_TMP"

for (( i = 0; i < ${#DATA_SERVERS[@]}; i+=2)); do
    j=$(( i + 1 ))
    ip=${DATA_SERVERS[$i]}
    community=${DATA_SERVERS[$j]}
    ping_response=$(bash $SCRIPT_PING $ip)
    if [ -n "$ping_response" ]; then
        bash $SCRIPT_SNMP $community $ip $CURRENT_DATE
    else 
        echo "$(date +"%Y-%m-%d %H:%M:%S") WARNING[/SNMP/main.sh] Server not response. IP: $ip" >> $LOG
    fi
done

#################### END ################################
# Delete folder tmp
if [ -d $FOLDER_RESPONSE_SNMP ]; then
    rm -r $FOLDER_TMP
fi

# If the script is run manually, the load spinner will come down.
if [ -n "$USERNAME" ]; then 
    kill $spinner_pid
    wait $spinner_pid
    echo -e "\nGetting consults SNMP... Done"
fi

#End time registration
echo "$(date +"%Y-%m-%d %H:%M:%S") INFO[/SNMP/main.sh] End consults SNMP of today" >> $LOG