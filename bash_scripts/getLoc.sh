#!/bin/bash

#####################################################
# 04.06.2020
#
# Fetch BS location information (?) from the sim 
# cards and save them to a log file. 
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

NOW=$(date +"%Y%m%d_%H%M%S")

while true
do
	date +"%Y%m%d_%H%M%S%N" | tee -a $NOW-getLoc_client1.txt
	sudo mmcli -m 0 | tee -a $NOW-getLoc_client1.txt
	sudo mmcli -m 0 --location-get | tee -a $NOW-getLoc_client1.txt
done
