#!/bin/bash

clear
username=ubuntu
homedir=`echo "/home/"$username`
vpnDir="/opt/cisco/anyconnect/bin"

# connect to VPN
cd $vpnDir
echo -e "\n\nFenerbahce999" | ./vpn -s connect https://asa-cluster.lrz.de
echo -e "Drones2018" | sudo -S ifconfig cscotun0 mtu 1500
ifconfig
