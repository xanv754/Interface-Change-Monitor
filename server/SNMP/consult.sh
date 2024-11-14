#!/bin/bash

FILEPATH=$1
community=$2
ip=$3
date=$4

echo "DATE=$date" >> "$FILEPATH"
echo "IP=$ip" >> "$FILEPATH"
echo "Community=$community" >> "$FILEPATH"
$COMMAND_SNMP $community $ip sysname >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifIndex >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifName >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifAlias >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifDescr >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifSpeed >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifHighSpeed >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifPhysAddress >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifType >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifOperStatus >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifAdminStatus >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifLastChange >> "$FILEPATH" && 
$COMMAND_SNMP $community $ip ifPromiscuousMode >> "$FILEPATH" &&
$COMMAND_SNMP $community $ip ifConnectorPresent >> "$FILEPATH" 

