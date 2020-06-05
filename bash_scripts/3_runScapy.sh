#!/bin/bash

#####################################################
# 04.06.2020
#
# Run scapy files at the VMs of NUC3 and Anelia 
# server.
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

tab=" --tab"
options=()
ipTUMVPN="129.187.211.11" # UPDATE !!!
oainuc3IP="10.100.1.101"
userID="ubuntu"

cmds[1]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3022 -X $userID@127.0.0.1 sudo ./scapy_sendPacket.py"
cmds[2]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3023 -X $userID@127.0.0.1 sudo ./scapy_sendPacket.py"
cmds[3]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3022 -X $userID@127.0.0.1 ssh -tt -X baltaci@$ipTUMVPN sudo ./scapy_sendPacket.py"
cmds[4]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3022 -X $userID@127.0.0.1 ssh -tt -X baltaci@$ipTUMVPN sudo ./scapy_sendPacket2.py"

for i in 1 2 3 4; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"" )
done

gnome-terminal "${options[@]}"

exit 0

