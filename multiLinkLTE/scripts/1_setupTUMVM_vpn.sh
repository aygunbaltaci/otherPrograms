#!/bin/bash

tab=" --tab"
options=()
oainuc3IP="10.100.1.101"

cmds[1]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3022 -X ubuntu@127.0.0.1 ./server_configNetwork.sh"

for i in 1; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"")
done

gnome-terminal "${options[@]}"

exit 0

