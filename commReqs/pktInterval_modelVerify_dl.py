#!/usr/bin/env python

from scapy.all import *
from scapy.utils import rdpcap
import time
from datetime import datetime
import math
import msvcrt
import numpy as np

# ======== variables
inputFileName = "straightAscend_flight1_downlink_cut.pcap"
outputFileName = "downlink2.pcap"
srcIP = "10.0.0.201" # !!! UPDATE !!! UPDATE THIS LINE EVERYTIME CLIENT HAS NEW IP !!! OTHERWISE, PACKETS MAY NOT REACH TO SERVER SIDE.
dstIP = "10.0.0.208" # !!! UPDATE !!! IP addr of server
srcPort = 47813 # UDP port at client
dstPort = 47811 # UDP port at server
date = datetime.now().strftime('%Y%m%d_%H%M%S')

def pkt_addLayers(pkt):
	pkt = UDP()/pkt
	pkt = IP()/pkt # 13082019
	pkt.time = time.time() * 100
	pkt[IP].src = srcIP
	pkt[IP].dst = dstIP
	pkt[UDP].sport = srcPort # Add a src port #
	
	return pkt

# ======== MAIN
def main():
	buffer, pkt = '', ''
	pktList, pktTime, pktLen, prevPkt, dataRate = [], [], [], [], []
	i, prevTime, totalPktLen = 0, 0, 0
	
	cameraControl = 'c' * 25
	takeOff_land = 'l' * 25 
	throttle =  't' * 1 + 'r' * 53
	pitch = 'p' * 25
	maxPktLen = 1486

	while True:
		videoInformation = 'v' * int(np.random.uniform(5000, 8000))
		if i % 1 == 0:
			buffer += (throttle)
		if i % 2 == 0:
			buffer += (pitch)
		if i % 5 == 0:
			buffer += (takeOff_land)
		if i % 6 == 0:
			buffer += (cameraControl)
			buffer += (videoInformation)
		
		if i % 2 == 0: # (not throttle is None or not pitch is None or cameraControl) and 
			k = 0
			l = True
				
			for j in range(math.ceil(len(buffer) / maxPktLen)):
				delayProb = np.random.uniform(0, 1)
				if delayProb > 0.8:
					sleepTime = np.random.uniform(0, 0.2)
					time.sleep(sleepTime)

				print("Generate packet")
				pkt = buffer[len(buffer) - 1 - maxPktLen:]
				buffer = buffer[:len(buffer) - 1 - maxPktLen]
				pkt = pkt_addLayers(pkt)
				timeDiff = float(pkt.time - prevTime) if prevTime != 0 else 0
				pktTime.append(timeDiff)
				pktLen.append(len(pkt))
				if int(prevTime / 100) != int(pkt.time / 100):
					print(int(prevTime / 100), int(pkt.time / 100))
					dataRate.append(totalPktLen * 8) # multiply by 8 to conver bytes to bits
					totalPktLen = 0
				else:
					dataRate.append("")
				totalPktLen += len(pkt)	
				pktList.append(pkt)
				prevTime = pkt.time
		i += 1
		print(len(pktTime))
		with open(date + '.csv', 'w') as outputFile:
			outputFile.write("{}, {}, {}\n".format("Packet Inter-arrival (ms)", "Packet Length (bytes)", "Data Rate (bps)"))
			for x in zip(pktTime, pktLen, dataRate):
				outputFile.write("{}, {}, {}\n".format(x[0], x[1], x[2]))
		
		if msvcrt.kbhit():
			break
		time.sleep(0.1)

	#wrpcap(outputFileName, pktList)
	print("Packet generation is completed!")

main()

############## USEFUL COMMANDS
'''
tcpreplay at client: sudo tcpreplay -q --preload-pcap -i cscotun0 straightAscend_flight1_downlink_scapyModified.pcap
tcpdump at client: sudo tcpdump -i cscotun0 -n udp port 2399 -vv -X -w test.pcap
tcpdump at server: sudo tcpdump -i 1 -n udp port 2399 -vv -X -w test3.pcap
scp at server: sudo scp test3.pcap ubuntulaptop@129.187.212.33:
increase mtu at client: sudo ifconfig cscotun0 mtu 1500

OTHER USEFUL SCAPY COMMANDS
print(pkt.summary()+"\n") # Print the layers of a packet

REMOVING A LAYER (IPv6ExtHdrRouting) FROM A PACKET, taken from https://stackoverflow.com/questions/46876196/how-to-remove-a-layer-from-a-packet-in-python-using-scapy
#pkt=IPv6()/IPv6ExtHdrRouting()/ICMPv6EchoRequest()
#pkt2=pkt[ICMPv6EchoRequest]
#pkt[IPv6].remove_payload()
#pkt /=pkt2

Generate packet from raw bytes: https://stackoverflow.com/questions/27262291/how-to-create-a-scapy-packet-from-raw-bytes
'''
