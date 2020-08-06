#!/bin/bash

#####################################################
# 04.06.2020
#
# Connect to the VPN.
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

clear
username=ubuntu
homedir=`echo "/home/"$username`
vpnDir="/opt/cisco/anyconnect/bin"

# connect to VPN
cd $vpnDir
echo -e "\n\n<add-vpn-password>" | ./vpn -s connect https://asa-cluster.lrz.de
echo -e "<add-PC-password>" | sudo -S ifconfig cscotun0 mtu 1500
ifconfig
