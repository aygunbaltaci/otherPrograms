#!/bin/bash

tab=" --tab"
options=()
oainuc3IP="10.100.1.101"
ipTUMVPN="129.187.212.100" # UPDATE !!!

cmds[1]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP scp -P 3022 ubuntu@127.0.0.1:/home/ubuntu/aygun_multiLinkMeas/measurements/* /home/oainuc3/aygun_droneMeas/measurements"
cmds[2]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP scp -P 3023 ubuntu@127.0.0.1:/home/ubuntu/aygun_multiLinkMeas/measurements/* /home/oainuc3/aygun_droneMeas/measurements"
#cmds[3]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP ssh -tt baltaci@$ipTUMVPN scp ubuntu@127.0.0.1:/home/ubuntu/aygun_multiLinkMeas/measurements/* /home/oainuc3/aygun_droneMeas/measurements"

for i in 1 2 3; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"" )
done

gnome-terminal "${options[@]}"

exit 0

