#!/bin/bash

#####################################################
# 04.06.2020
#
# Save the measurement results from the VMs to the 
# main OS in NUC3.
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

tab=" --tab"
options=()
oainuc3IP="10.100.1.101"
ipTUMVPN="129.187.212.100" # UPDATE !!!

cmds[1]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP scp -P 3022 ubuntu@127.0.0.1:/home/ubuntu/aygun_multiLinkMeas/measurements/* /home/oainuc3/aygun_droneMeas/measurements"
cmds[2]="sshpass -p <add-PC-password> ssh -tt -X oainuc3@$oainuc3IP scp -P 3023 ubuntu@127.0.0.1:/home/ubuntu/aygun_multiLinkMeas/measurements/* /home/oainuc3/aygun_droneMeas/measurements"

for i in 1 2; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"" )
done

gnome-terminal "${options[@]}"

exit 0

