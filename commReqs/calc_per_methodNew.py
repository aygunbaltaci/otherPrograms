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
maxPSN = 4095
lateArrival_threshold = 45 # number of packets that can arrive late. Used to correctly calculate number of packets and packet loss. Because, late arrivals can mess up the calculations (e.g. if a packet with PSN 4095 arrives after a packet with PSN 0, then calculators will think there are 4094 lost packets).

# variables for calculate_bps()
startPkt = 0 # packet num of the packet which you want to begin the calculations

fileDate = datetime.now().strftime('%Y%m%d_%H%M%S_')
outputFile = 'perStats'
outputFileOverall = 'overallResults'
outputFileSort = '_pktsSorted'
outputFileLoss = '_lossPkts'
outputFileFormat = '.csv'
outputFileName = outputFileBeginWord + fileDate + outputFile + outputFileOverall + outputFileFormat
outputFileNameSort = outputFileBeginWord + fileDate + outputFile + outputFileSort + outputFileFormat
outputFileNameLoss = outputFileBeginWord + fileDate + outputFile + outputFileLoss + outputFileFormat

def writeNumOfPackets(minSqnNum, maxSqnNum, pktCount2, timeStampRef2, numPktsPerSec): 
    if minSqnNum == 99999 and maxSqnNum == 0: # there is no packet with PSN during the time interval
        minSqnNum = 0 
        maxSqnNum = 0
    if maxSqnNum != minSqnNum:
        pktCount2 += maxSqnNum - minSqnNum + 1 # if they are equal, that means there is only 1 packet
    numPktsPerSec.append(pktCount2)
    print("Time: %d, # of packets: %d" %(timeStampRef2, pktCount2))
    minSqnNum = 99999
    maxSqnNum = 0
    pktCount2 = 0 
    return numPktsPerSec, minSqnNum, maxSqnNum, pktCount2

# ======== modify sniffed packets
def packetStats():
    sqnNum = 0 
    prevSqnNum = 0
    prevSqnNum2 = 0
    pktLossCnt = 0
    prevTime = 0
    timeStamp = 0
    secCnt = 0
    numPktsPerSec = []
    pktLossPerSec = []
    lastPSNPerSec = []
    prevPktCount = 0
    pktCount = 0
    pktCount2 = 0
    cutData_sqn = []
    cutData_time = []
    organizedData = pd.DataFrame()

    data = pd.read_csv(perInputFileName)
    
    # write header to output file
    with open(outputFileName, 'a') as outputFile:
        outputFile.write('time, # of total packets, loss packets, per (%)\n')

    # find the first PSN
    for k in range(len(data.iloc[:, 1])):
        if not math.isnan(data.iloc[k, 1]):
            prevSqnNum = data.iloc[k, 1]
            prevSqnNum2 = data.iloc[k, 1]
            break

    timeStampRef2 = int(data.iloc[0, 0])

    # calculate number of seconds
    for i in range(len(data.iloc[:, 0])):
        timeStamp = int(data.iloc[i, 0]) 
        if int(timeStamp) - int(timeStampRef2) >= 1: 
            for j in range(int(timeStamp) - int(timeStampRef2)):
                secCnt += 1
                timeStampRef2 = int(timeStamp)

    # initialize empty arrays 
    for i in range(secCnt):
        numPktsPerSec.append(0)
        pktLossPerSec.append(0)

    # calculate # of rx packets per second only from Wireshark
    timeStampRef2 = int(data.iloc[0, 0])
    secCnt = 0
    for i in range(len(data.iloc[:, 0])):
        pktCount += 1 
        timeStamp = int(data.iloc[i, 0])
        if int(timeStamp) - int(timeStampRef2) >= 1:
            numPktsPerSec[secCnt] = pktCount
            if int(timeStamp) - int(timeStampRef2) > 1:
                for j in range(int(timeStamp) - int(timeStampRef2) - 1):
                    secCnt += 1  
                    numPktsPerSec[secCnt] = 0.1 # 0.1 just to avoid 0 division error
                    
            timeStampRef2 = int(timeStamp)
            pktCount = 0
            secCnt += 1  
    
    # reorder packets according to PSNs
    timeStampRef2 = int(data.iloc[0, 0])
    for m in range (len(data.iloc[:, 1])):
        cutData_time.append(data.iloc[m, 0])
        cutData_sqn.append(data.iloc[m, 1])
        timeStamp = int(data.iloc[m, 0])
        if data.iloc[m, 1] == 4095 or data.iloc[m, 0] == data.iloc[-1, 0] or int(timeStamp) - int(timeStampRef2) >= 1:
            cutData_lastTime = cutData_time[-1]
            cutData_lastSqn = cutData_sqn[-1]
            cutData_time.pop()
            cutData_sqn.pop()
            insertData = {'time': cutData_time, 'sqn': cutData_sqn}
            organizedData = pd.DataFrame(insertData)
            organizedData = organizedData.sort_values('sqn')
            organizedData.to_csv(outputFileNameSort, mode = 'a')
            cutData_time, cutData_sqn = [], []
            cutData_time.append(cutData_lastTime)
            cutData_sqn.append(cutData_lastSqn)
            if int(timeStamp) - int(timeStampRef2) >= 1:
                timeStampRef2 = int(timeStamp)
            
            # calculate # of loss packets per second
            for i in range (len(organizedData['sqn'])):
                if not math.isnan(organizedData['sqn'].values[i]): # ignore empty cells in csv
                    sqnNum = organizedData['sqn'].values[i]
                    if abs(sqnNum - prevSqnNum) > 1 and abs(sqnNum - prevSqnNum) < 100: # do not count losses more than 100 packets. no clue what might have happened in between.
                        for j in range (abs(int(sqnNum) - int(prevSqnNum))):
                            print("lost packet: t = %f, sqnNum = %d" %(organizedData['time'].values[i - 1], (sqnNum - j - 1)))
                            with open(outputFileNameLoss, 'a') as outputFileLoss:
                                outputFileLoss.write("lost packet: t = %f, sqnNum = %d\n" %(organizedData['time'].values[i - 1], (sqnNum - j - 1)))
                            pktLossPerSec[int(organizedData['time'].values[i - 1])] += 1 # add loss pkts
                            numPktsPerSec[int(organizedData['time'].values[i - 1])] += 1 # add loss pkts to total pkt count 
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