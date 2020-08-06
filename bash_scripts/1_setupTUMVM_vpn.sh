#!/bin/bash

#####################################################
# 04.06.2020
#
# Connect to the 1st VM of NUC3 to get connected to 
# Anelia server. This will connect Anelia to VPN (?).  
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

tab=" --tab"
options=()
oainuc3IP="10.100.1.101"

cmds[1]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3022 -X ubuntu@127.0.0.1 ./server_configNetwork.sh"

for i in 1; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"")
done

gnome-terminal "${options[@]}"

exit 0

