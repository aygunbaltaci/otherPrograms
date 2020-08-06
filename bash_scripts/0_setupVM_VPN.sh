#!/bin/bash

#####################################################
# 04.06.2020
#
# Connect to the VMs of NUC3 and connect them to 
# VPNs
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

tab=" --tab"
options=()
ipTUMVPN="172.24.25.113"
oainuc3IP="10.100.1.101"

cmds[1]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3022 -X ubuntu@127.0.0.1 ./configNetwork.sh"
cmds[2]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3023 -X ubuntu@127.0.0.1 sudo openconnect https://asa-cluster.lrz.de -u '!ga83pod'"

for i in 1 2; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"" )
done

gnome-terminal "${options[@]}"

exit 0

