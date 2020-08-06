#!/bin/bash

#####################################################
# 04.06.2020
#
# Start the data transfer between VMs and the server.
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

tab=" --tab"
options=()
ipTUMVPN="129.187.211.11" # UPDATE!!!
oainuc3IP="10.100.1.101"
userID="ubuntu"
saveDate=`date +"%Y%m%d_%H%M%S"`

cmds[1]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sudo -S <<< \"<add-PC-password>\" ./GPSLog aygun_droneMeas/measurements/$saveDate-gpsLog.txt"
cmds[2]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3022 -X root@127.0.0.1 screen"
cmds[3]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3023 -X root@127.0.0.1 screen"
cmds[4]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP sshpass -p <add-PC-password> ssh -tt -p 3022 -X ubuntu@127.0.0.1 ssh -tt -X baltaci@$ipTUMVPN screen"

for i in 1 2 3 4; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"" )
done

gnome-terminal "${options[@]}"

exit 0

