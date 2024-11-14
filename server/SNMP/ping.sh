#!/bin/bash

ip=$1
SAVE=$2

ping=$($COMMAND_PING $ip 1)
status=$(echo $ping | grep "is alive")
echo $status