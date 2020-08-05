#!/bin/bash

tab=" --tab"
options=()
ipTUMVPN="129.187.211.11" # UPDATE!!!
oainuc3IP="10.100.1.101"
userID="ubuntu"
saveDate=`date +"%Y%m%d_%H%M%S"`

cmds[1]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sudo -S <<< \"Drones2018\" ./GPSLog aygun_droneMeas/measurements/$saveDate-gpsLog.txt"
cmds[2]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3022 -X root@127.0.0.1 screen"
cmds[3]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3023 -X root@127.0.0.1 screen"
cmds[4]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3022 -X ubuntu@127.0.0.1 ssh -tt -X baltaci@$ipTUMVPN screen"

for i in 1 2 3 4; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"" )
done

gnome-terminal "${options[@]}"

exit 0

