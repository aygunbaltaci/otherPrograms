#!/bin/bash

tab=" --tab"
options=()
ipTUMVPN="172.24.25.113"
oainuc3IP="10.100.1.101"

cmds[1]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3022 -X ubuntu@127.0.0.1 ./configNetwork.sh"
#cmds[2]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3022 -X root@127.0.0.1 nano scapy_sendPacket.py"
cmds[3]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3023 -X ubuntu@127.0.0.1 sudo openconnect https://asa-cluster.lrz.de -u '!ga83pod'"
#cmds[4]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3023 -X root@127.0.0.1 nano scapy_sendPacket.py"
#cmds[5]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3022 -X ubuntu@127.0.0.1 ssh -tt -X baltaci@$ipTUMVPN nano scapy_sendPacket.py"
#cmds[6]="sshpass -p Drones2018 ssh -tt -X oainuc3@$oainuc3IP sshpass -p Drones2018 ssh -tt -p 3022 -X ubuntu@127.0.0.1 ssh -tt -X baltaci@$ipTUMVPN nano scapy_sendPacket2.py"

for i in 1 2 3 4 5 6; do
  options+=($tab -e "bash -c \"${cmds[i]} ; bash\"" )
done

gnome-terminal "${options[@]}"

exit 0

