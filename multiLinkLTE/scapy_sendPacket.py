#!/usr/bin/env python

from scapy.all import *
from scapy.utils import rdpcap
import time
import math

# ======== variables
inputFileName = "straightAscend_flight1_downlink_cut.pcap"
outputFileName = "downlink1.pcap"
srcIP = "129.187.178.185" # !!! UPDATE !!! UPDATE THIS LINE EVERYTIME CLIENT HAS NEW IP !!! OTHERWISE, PACKETS MAY NOT REACH TO SERVER SIDE.
dstIP = "129.187.212.1" # !!! UPDATE !!! IP addr of server
srcPort = 47813 # UDP port at client
dstPort = 47811 # UDP port at server
macIPUDPOverhead = 28 # # num of extra bytes from IP and UDP layers

# variables for MTU limitation. leftOver bytes: remaining bytes from packets due to MTU limitation.
maxMTU = 1500
artifDelay = 0.002000 # artificial delay for extra packets generated, 2 msec
addLeftOverBytes = False # whether to add leftover bytes to end of already-existing packets where len(pkt) > maxMTU
leftOverBytes_genNewPkts = False # whether to generate new packets out of leftover bytes

# load balancing variables
loadBal = False # load balancing feature. Only half of the data will be generated. Select odd or even below
loadBalPat_even = False # packets with even packet numbers will be written. Valid only if loadBal is True

# packet splitting variables
pSplit = True
ps_send2ndHalf = False # send only the 2nd half of packets for packet splitting method. Otherwise, 1st half to be sent

# ======== shape packet lengths
def resize_packet(pkt, maxMTU, clonedPkt, macIPUDPOverhead, leftoverData):
	clonedPkt = str(pkt[PPI]) # convert pkt into string
	
	# Packet splitting
	if pSplit == True:
		if ps_send2ndHalf == True: 
			leftoverData = leftoverData + clonedPkt[:len(clonedPkt)/2] # collect extra bytes
			clonedPkt = clonedPkt[len(clonedPkt)/2:] # shrink the size of packet to maxMTU and reduce extra bytes to allocate IP & UDP layers later on
		else:
			leftoverData = leftoverData + clonedPkt[len(clonedPkt)/2:] # collect extra bytes
			clonedPkt = clonedPkt[:len(clonedPkt)/2] # shrink the size of packet to maxMTU and reduce extra bytes to allocate IP & UDP layers later on
	
	# MTU limitation
	if len(clonedPkt) > maxMTU: # dissect the packet if it exceeds the max MTU size
		leftoverData = leftoverData + clonedPkt[maxMTU:] # collect extra bytes
		clonedPkt = clonedPkt[:maxMTU] # shrink the size of packet to maxMTU and reduce extra bytes to allocate IP & UDP layers later on
	
	# Add leftover bytes to end of already-existing packets
	if addLeftOverBytes == True and len(clonedPkt) < maxMTU:  # send leftover bytes if enabled && packet len < maxMTU
		emptySize = maxMTU - len(clonedPkt) # find out number of leftover bytes that can be allocated to packet
		if emptySize < len(leftoverData): # leftover bytes exceeding available space in pkt
			#print("len of leftoverdata before = %d" %len(leftoverData))
			clonedPkt_origLen = len(clonedPkt) # store original length of pkt before extending its size, original length needed to determine what portion of leftover data to keep
			clonedPkt = clonedPkt + leftoverData[:maxMTU - clonedPkt_origLen] # place portion of leftover bytes to pkt
			leftoverData = leftoverData[maxMTU - clonedPkt_origLen:] # delete allocated bytes from leftover str
			#print("len of leftoverdata after = %d" %len(leftoverData))
		else: # all leftover bytes can be allocated in packet
			clonedPkt = clonedPkt + leftoverData # add leftover bytes to packet, reduce the size to allocate IP & UDP layers later on
			leftoverData = ''
	
	# Remove bytes from packets for extra bytes from IP&UDP layers, to keep packet length same
        #leftOverData = leftOverData + clonedPkt[len(clonedPkt) - macIPUDPOverhead:] # enable this line if you want to send all bytes from original packets. It is disabled now to keep total bitrate same
	clonedPkt = clonedPkt[:len(clonedPkt) - macIPUDPOverhead]
	
	return clonedPkt, leftoverData

# renegerate manipulated packets
def renegerate_packet(pkts, pkt_list, clonedPkt, counter, timestamp, leftOverBytes_timestamp):
	clonedPkt = UDP()/clonedPkt
	clonedPkt = IP()/clonedPkt # 13082019
	clonedPkt[IP].src = srcIP
	clonedPkt[IP].dst = dstIP
	clonedPkt[UDP].sport = srcPort # Add a src port #
	clonedPkt[UDP].dport = dstPort # Add a dest port #
	if leftOverBytes_timestamp == False:
		timestamp = pkts[counter].time
	clonedPkt.time = timestamp # Keep original timestamps on packets
	pkt_list.append(clonedPkt)
	return timestamp

# ======== MAIN
def main():
	pkts = rdpcap(inputFileName)
	counter = 0
	pkt_list = []
	leftoverData = ''
	clonedPkt = ''
	timestamp = 0
	print("Packet manipulation has begun. It will take a while...")
	for pkt in pkts:
		if loadBal == True:
			if loadBalPat_even == True:
				if counter % 2 != 0:
					clonedPkt, leftoverData = resize_packet(pkt, maxMTU, clonedPkt, macIPUDPOverhead, leftoverData)
					timestamp = renegerate_packet(pkts, pkt_list, clonedPkt, counter, timestamp, False)
			else:
				if counter % 2 == 0:
					clonedPkt, leftoverData = resize_packet(pkt, maxMTU, clonedPkt, macIPUDPOverhead, leftoverData)
					timestamp = renegerate_packet(pkts, pkt_list, clonedPkt, counter, timestamp, False)
		else: # no load balancing
			clonedPkt, leftoverData = resize_packet(pkt, maxMTU, clonedPkt, macIPUDPOverhead, leftoverData)
			timestamp = renegerate_packet(pkts, pkt_list, clonedPkt, counter, timestamp, False)
		counter += 1
	print("Leftover bytes: %d" %len(leftoverData))
	leftoverPktNum = int(math.ceil(float(len(leftoverData)) / (maxMTU))) # find out how many extra packets to be generated from leftover bytes
	lastPktLen = len(leftoverData) % (maxMTU)
	startByte = 0
	if leftOverBytes_genNewPkts == True:
		print("Leftover Packet Number=%d \n" %leftoverPktNum)
		print("Last packet len=%d" %lastPktLen)
		print("Adding leftover packets to pcap...") 
		for i in range(leftoverPktNum):
			if i == leftoverPktNum - 1:
				clonedPkt = leftoverData[startByte:startByte + lastPktLen - macIPUDPOverhead]
			else:
				clonedPkt = leftoverData[startByte:startByte + maxMTU - macIPUDPOverhead]
				startByte += maxMTU
			timestamp += artifDelay
			timestamp = renegerate_packet(pkts, pkt_list, clonedPkt, counter, timestamp, True)
	wrpcap(outputFileName, pkt_list)
	print("Packet manipulation is completed!")

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
