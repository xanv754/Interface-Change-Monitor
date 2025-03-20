#!/bin/bash
COMMUNITY=$1
IP=$2
DATE=$3

CURRENT_PATH="$(pwd)/data/$DATE"
LOG="$(cd .. && pwd)/system.log"
OUTPUT_ROOT="$CURRENT_PATH/"$IP"_$COMMUNITY"
OUTPUT_SYSNAME=""$OUTPUT_ROOT"_sysname"
OUTPUT_IFINDEX=""$OUTPUT_ROOT"_ifIndex"
OUTPUT_IFNAME=""$OUTPUT_ROOT"_ifName"
OUTPUT_IFDESCR=""$OUTPUT_ROOT"_ifDescr"
OUTPUT_IFALIAS=""$OUTPUT_ROOT"_ifAlias"
OUTPUT_IFHIGHSPEED=""$OUTPUT_ROOT"_ifHighSpeed"
OUTPUT_IFOPERSTATUS=""$OUTPUT_ROOT"_ifOperStatus"
OUTPUT_IFADMINSTATUS=""$OUTPUT_ROOT"_ifAdminStatus"

function delete_files {
    if [ -f $OUTPUT_SYSNAME ]; then
        rm $OUTPUT_SYSNAME
    fi
    if [ -f $OUTPUT_IFINDEX ]; then
        rm $OUTPUT_IFINDEX
    fi
    if [ -f $OUTPUT_IFNAME ]; then
        rm $OUTPUT_IFNAME
    fi
    if [ -f $OUTPUT_IFDESCR ]; then
        rm $OUTPUT_IFDESCR
    fi
    if [ -f $OUTPUT_IFALIAS ]; then
        rm $OUTPUT_IFALIAS
    fi
    if [ -f $OUTPUT_IFHIGHSPEED ]; then
        rm $OUTPUT_IFHIGHSPEED
    fi
    if [ -f $OUTPUT_IFOPERSTATUS ]; then
        rm $OUTPUT_IFOPERSTATUS
    fi
    if [ -f $OUTPUT_IFADMINSTATUS ]; then
        rm $OUTPUT_IFADMINSTATUS
    fi
}

if [ -d $CURRENT_PATH ]; then
    $COMMAND_SNMP $COMMUNITY $IP sysname | awk -F '= STRING: ' '{print substr($2, 1, 11)}' >> $OUTPUT_SYSNAME
    $COMMAND_SNMP $COMMUNITY $IP ifIndex | awk -F '= INTEGER:' '{print $2}' >> $OUTPUT_IFINDEX
    $COMMAND_SNMP $COMMUNITY $IP ifName | awk -F '= STRING:' '{print $2}' >> $OUTPUT_IFNAME
    $COMMAND_SNMP $COMMUNITY $IP ifDescr | awk -F '= STRING:' '{print $2}' >> $OUTPUT_IFDESCR
    $COMMAND_SNMP $COMMUNITY $IP ifAlias | awk -F '= STRING:' '{print $2}' >> $OUTPUT_IFALIAS
    $COMMAND_SNMP $COMMUNITY $IP ifHighSpeed | awk -F '= Gauge32:' '{print $2}' >> $OUTPUT_IFHIGHSPEED
    $COMMAND_SNMP $COMMUNITY $IP ifOperStatus | awk -F '= INTEGER:' '{print $2}' >> $OUTPUT_IFOPERSTATUS
    $COMMAND_SNMP $COMMUNITY $IP ifAdminStatus | awk -F '= INTEGER:' '{print $2}' >> $OUTPUT_IFADMINSTATUS

    total_register_ifIndex=$(cat $OUTPUT_IFINDEX | wc -l)
    if [ $total_register_ifIndex -gt 0 ]; then
        # Check if the ifName and ifIndex are the same length
        total_register_ifName=$(cat $OUTPUT_IFNAME | wc -l)
        if [ $total_register_ifName -eq $total_register_ifIndex ]; then
            # Check if the ifDescr and ifIndex are the same length
            total_register_ifDescr=$(cat $OUTPUT_IFDESCR | wc -l)
            if [ $total_register_ifDescr -eq $total_register_ifIndex ]; then
                # Check if the ifAlias and ifIndex are the same length
                total_register_ifAlias=$(cat $OUTPUT_IFALIAS | wc -l)
                if [ $total_register_ifAlias -eq $total_register_ifIndex ]; then
                    # Check if the ifHighSpeed and ifIndex are the same length
                    total_register_ifHighSpeed=$(cat $OUTPUT_IFHIGHSPEED | wc -l)
                    if [ $total_register_ifHighSpeed -eq $total_register_ifIndex ]; then
                        # Check if the ifOperStatus and ifIndex are the same length
                        total_register_ifOperStatus=$(cat $OUTPUT_IFOPERSTATUS | wc -l)
                        if [ $total_register_ifOperStatus -eq $total_register_ifIndex ]; then
                            # Check if the ifAdminStatus and ifIndex are the same length
                            total_register_ifAdminStatus=$(cat $OUTPUT_IFADMINSTATUS | wc -l)
                            if [ $total_register_ifAdminStatus -eq $total_register_ifIndex ]; then
                                sysname=$(cat $OUTPUT_SYSNAME)
                                paste -d ';' $OUTPUT_IFINDEX $OUTPUT_IFNAME $OUTPUT_IFDESCR $OUTPUT_IFALIAS $OUTPUT_IFHIGHSPEED $OUTPUT_IFOPERSTATUS $OUTPUT_IFADMINSTATUS > ""$OUTPUT_ROOT"_$sysname"
                                delete_files
                            else 
                                echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] List of ifAdminStatus does not match the ifIndex. IP: $IP, community: $COMMUNITY" >> $LOG
                                delete_files
                            fi
                        else 
                            echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] List of ifOperStatus does not match the ifIndex. IP: $IP, community: $COMMUNITY" >> $LOG
                            delete_files
                        fi
                    else 
                        echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] List of ifHighSpeed does not match the ifIndex. IP: $IP, community: $COMMUNITY" >> $LOG
                        delete_files
                    fi
                else 
                    echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] List of ifAlias does not match the ifIndex. IP: $IP, community: $COMMUNITY" >> $LOG
                    delete_files
                fi
            else 
                echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] List of ifDescr does not match the ifIndex. IP: $IP, community: $COMMUNITY" >> $LOG
                delete_files
            fi
        else 
            echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] List of ifName does not match the ifIndex. IP: $IP, community: $COMMUNITY" >> $LOG
            delete_files
        fi
    else
        echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] List of ifIndex not found. IP: $IP, community: $COMMUNITY" >> $LOG
        delete_files
    fi
else
    echo "$(date +"%Y-%m-%d %H:%M:%S") ERROR[/SNMP/snmp.sh] Directory of tmp response snmp not exists" >> $LOG
    delete_files
fi
