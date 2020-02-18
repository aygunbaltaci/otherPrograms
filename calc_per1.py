#!/usr/bin/env python

from scapy.all import *
from scapy.utils import rdpcap
import time
import math
from binascii import unhexlify
import numpy as np
import pandas as pd

# ======== variables
perInputFileName = "sqn_dl.csv" # use this command to generate sqn list file: 'tshark -r flight4_wifi_ul.pcap -e frame.time_relative -e wlan.seq -Tfields | tee sqn_ul.csv'
outputFileBeginWord = 'dl_'
# Variables for checkIdenticalPkt()
identicalPkt_pktNum = 2 # Enter the packet num (in Wireshark) of the packet that its unduplicates to be checked 
printIdenticalPkts = True # Print stats of found identical packets 
printNonIdenticalPkts = True # Print stats of found nonidentical packets

# variables for calculate_bps()
startPkt = 0 # packet num of the packet which you want to begin the calculations

# variables for calculate_per()
leftoverTime_freq = 1000 # how often elapsed and leftover time to be printed on the terminal. Once per # of loops, # of loops to be defined here

fileDate = datetime.now().strftime('%Y%m%d_%H%M%S_')
outputFile = 'perStats'
outputFileLossPkts = '_lossPkts'
outputFileErr = '_potentialLostFrames'
outputFileSort = '_pktsSorted'
outputFilePER = '_PER'
outputFileFormat = '.csv'
outputDir = ''
outputFileName = outputFileBeginWord + fileDate + outputFile + outputFileFormat
outputFileNameErr = outputFileBeginWord + fileDate + outputFile + outputFileErr + outputFileFormat
outputFileNameSort = outputFileBeginWord + fileDate + outputFile + outputFileSort + outputFileFormat
outputFileNamePER = outputFileBeginWord + fileDate + outputFile + outputFilePER + outputFileFormat
outputFileNameLossPkts = outputFileBeginWord + fileDate + outputFile + outputFileLossPkts + outputFileFormat
inputFileDelimeter = ','
outputFileDelimeter = ' '
defaultEncoding = 'utf-8-sig'   

# ======== modify sniffed packets
def packetStats():
    sqnNum = 0 
    prevSqnNum = 0
    pktLossCnt = 0
    prevTime = 0
    timeStamp = 0
    secCnt = 0
    numPktsPerSec = []
    pktLossPerSec = []
    prevPktCount = 0
    pktCount = 0
    pktCount2 = 0
    cutData_sqn = []
    cutData_time = []
    organizedData = pd.DataFrame()

    data = pd.read_csv(perInputFileName)
    
    prevSqnNum = data.iloc[0, 1]
    timeStampRef2 = int(data.iloc[0, 0])
    
    with open(outputFileName, 'a') as outputFile:
        outputFile.write('time, # of total packets, loss packets, per (%)\n')
    
    # calculate # of packets per second
    for i in range(len(data.iloc[:, 0])):
        timeStamp = int(data.iloc[pktCount, 0]) # data.iloc[0, 0] correlates to the 2nd entry in csv input, therefore it counts 1 less pkt in the first time interval. 
        pktCount += 1
        if int(timeStamp) - int(timeStampRef2) >= 1: 
            numPktsPerSec.append(pktCount2)
            print("Time: %d, # of packets: %d" %(timeStampRef2, pktCount2))
            if int(timeStamp) - int(timeStampRef2) > 1:
                for j in range(int(timeStamp) - int(timeStampRef2) - 1):
                    numPktsPerSec.append(0.1) # 0.1 just to avoid 0 division error
            timeStampRef2 = int(timeStamp)
            pktCount2 = 0  
        if i == len(data.iloc[:, 0]) - 1: # save the num of pkts from last second
            numPktsPerSec.append(pktCount2 + 1) # +1 to count the last packet as well
            print("Time: %d, # of packets: %d" %(timeStampRef2, pktCount2 + 1))
            timeStampRef2 = int(timeStamp)
            pktCount2 = 0
        pktCount2 += 1
    
    # initialize empty array for PER 
    for i in range(len(numPktsPerSec)):
        pktLossPerSec.append(0)
    
    # reorder packets according to PSNs
    for m in range (len(data.iloc[:, 1])):
        cutData_time.append(data.iloc[m, 0])
        cutData_sqn.append(data.iloc[m, 1])
        if data.iloc[m, 1] == 4095 or data.iloc[m, 0] == data.iloc[-1, 0]:
            insertData = {'time': cutData_time, 'sqn': cutData_sqn}
            organizedData = pd.DataFrame(insertData)
            organizedData = organizedData.sort_values('sqn')
            organizedData.to_csv(outputFileNameSort, mode = 'a')
            cutData_time, cutData_sqn = [], []
            
            # calculate # of loss packets per second
            for i in range (len(organizedData['sqn'])):
                if not math.isnan(organizedData['sqn'].values[i]): # ignore empty cells in csv
                    sqnNum = organizedData['sqn'].values[i]
                    if sqnNum - prevSqnNum > 1:
                        for j in range (int(sqnNum) - int(prevSqnNum)):
                            pktLossPerSec[int(organizedData['time'].values[i - 1])] += 1
                            print("lost packet: t = %f, sqnNum = %d" %(organizedData['time'].values[i - 1], (sqnNum - j - 1)))    
                            
                    prevSqnNum = sqnNum
    with open(outputFileName, 'a') as outputFile:
        for l in range (len(numPktsPerSec)):
            outputFile.write('%d, %d, %d, %f\n' %(l + 1, numPktsPerSec[l], pktLossPerSec[l], (pktLossPerSec[l]/numPktsPerSec[l]) * 100))               
packetStats()

############## COMMANDS
'''
tshark -r straightAscend1_uplink.pcap -e frame.time_relative -e wlan.seq -Tfields | tee sqn_ul.csv
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
