#!/bin/bash
NOW=$(date +"%Y%m%d_%H%M%S")


while true
do
	date +"%Y%m%d_%H%M%S%N" | tee -a $NOW-getLoc_client1.txt
	sudo mmcli -m 0 | tee -a $NOW-getLoc_client1.txt
	sudo mmcli -m 0 --location-get | tee -a $NOW-getLoc_client1.txt
done
