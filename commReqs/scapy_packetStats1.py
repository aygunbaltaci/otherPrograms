#!/usr/bin/env python

from scapy.all import *
from scapy.utils import rdpcap
import time
import math
from binascii import unhexlify
import numpy as np
import pandas as pd

# ======== variables
inputFileName = "link1/pcap_packets/link1_dl_end_noTcpSshIcmp.pcap"
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
outputDir = 'logs'
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
    tick = time.time()
    pkts=rdpcap(inputFileName)
    print("Pcap file is read. Elapsed time: %s" %(time.time() - tick))
    #pkts2=rdpcap(inputFileName2)
    #print("Second pcap file is read. Elapsed time: %s" %(time.time() - tick))
    bps_startPacket = startPkt 
    totalBits = 0
    startTime = pkts[bps_startPacket].time * 100 # multiply by 100 to avoid decimal operations
    cumTime = startTime 
    deltaTime = 0
    bps = []
    cumPer = []
    cumFoundPkt = [] 
    cumLossPkt = []
    loopCnt = 0
    loopCnt2 = 0
    t0 = time.time()
    t1 = []
    t2 = []
    loopCounter = 0 # for process completion percentage and elapsed time calculator
    printStatFreq = 1000 # 1/frequency (per loop) of process completion stats to be printed
    foundPkt = False 
    lossPkt = False
    numFoundPkt = 0
    numLossPkt = 0
    per = 0
    findFirstPkt = True
    prevByte = ''
    currByte = ''
    counter = 0
    pktCount = 0
    prevPktCount = 0
    sqnNumList = []
    sqnNum = 0
    prevSqnNum = 0
    prevPktLen = 0
    pktLen = 0
    numDiff = 0
    prevNumDiff = 99999
    timeStampRef = float(pkts[0].time)
    timeStampRef2 = float(pkts[0].time)
    numPktsPerSec = []
    secCnt = 0
    firstRun = True 
    
    with open(outputDir + os.sep + outputFileName, 'a') as outputFile:
        outputFile.write('pktNum, sqnNumList, timeStamp\n')
    with open(outputDir + os.sep + outputFileNameErr, 'a') as outputFile:
        outputFile.write('Potentially lost frame! PktNum:\n')
        
    for pkt in pkts:
        pktCount += 1
        timeStamp = float(pkt.time)
        # calculate num of pkts per second 
        if int(timeStamp - timeStampRef2) > secCnt: 
            numPktsPerSec.append(pktCount - prevPktCount)
            prevPktCount = pktCount
            secCnt += 1
            
        pktLen = len(pkt)
        if len(pkt) == 1348 and len(pkts[pktCount]) != 172: 
            with open(outputDir + os.sep + outputFileNameErr, 'a') as outputFile:
                outputFile.write('%d\n' %pktCount)
        if pkt.proto == 17: # filter only UDP packets
            pkt = str(pkt)
            for byteCount in range(len(pkt)):
                if byteCount + 4 <= len(pkt) and pkt[byteCount:byteCount + 5].isdigit(): #currByte.isdigit() and pkt[counter + 1].isdigit() and pkt[counter + 2].isdigit() and pkt[counter + 3].isdigit() and pkt[counter + 4].isdigit():
                    #print('pkt num = %d, sqn num = %s' %(pktCount, (pkt[byteCount:byteCount + 5])))
                    sqnNumList.append(pkt[byteCount:byteCount + 5])
            
            # find sqn num that is closest to the prev one
            for i in sqnNumList:
                numDiff = abs(int(i) - prevSqnNum)
                if numDiff < prevNumDiff: 
                    sqnNum = int(i)
                    prevNumDiff = numDiff
                    
            if len(sqnNumList) != 0:
                with open(outputDir + os.sep + outputFileName, 'a') as outputFile:
                    outputFile.write('%d, %d, %f\n' %(pktCount, sqnNum, timeStamp))
                sqnNumList = []
                prevSqnNum = sqnNum
                prevNumDiff = 99999
        prevPktLen = pktLen
        
    inputData = pd.read_csv(outputDir + os.sep + outputFileName)
    inputData = inputData.sort_values(' sqnNumList')
    print(inputData)
    inputData.to_csv(outputDir + os.sep + outputFileNameSort)
    
    sortedSqnNum = 0
    lossPktCnt = 0
    lossPktTimeStamps = []
    prevSortedSqnNum = inputData.loc[0, ' sqnNumList']
    #print(inputData.loc[:, ' sqnNumList'])
    for row in inputData.itertuples(): #range(len(inputData)): #inputData.itertuples(name = ' sqnNumList'): # (len(inputData.loc[:, ' sqnNumList'])):
        if row[2] - prevSortedSqnNum > 1:
            relTime = row[3] - timeStampRef
            print("Loss packet #: %d, referenceTime: %f" %(row[1], relTime))
            lossPktTimeStamps.append(int(relTime))
            lossPktCnt += 1
            with open(outputDir + os.sep + outputFileNameErr, 'a') as outputFile:
                outputFile.write("Loss packet #: %d, referenceTime: %f\n" %(row[1], relTime))
        prevSortedSqnNum = row[2]
    print("\nTotal num of packets: %d, total num of lost packets: %d" %(len(pkts), lossPktCnt))
    
    lossCounter = 0
    pktLossPerSec = []
    PER = []
    # calculate PER per second:
    for i in range(1, len(numPktsPerSec) + 1):
        for j in range(len(lossPktTimeStamps)):
            if i == lossPktTimeStamps[j]:
                lossCounter += 1
        pktLossPerSec.append(lossCounter)
        lossCounter = 0
    print("\nPPS: %s" %numPktsPerSec)
    print("Loss PPS: %s" %pktLossPerSec)
    for i in range(len(numPktsPerSec)):
        PER.append((pktLossPerSec[i]/numPktsPerSec[i]) * 100)
    print("PER per sec: %s" %PER)
    #calculate_per(pkts, pkts2, cumPer, cumFoundPkt, cumLossPkt, loopCnt, loopCnt2, t0, t1, t2, loopCounter, printStatFreq, foundPkt, lossPkt, numFoundPkt, numLossPkt, per, findFirstPkt)
    with open(outputDir + os.sep + outputFileNamePER, 'a') as outputFile:
        outputFile.write('Time, PPS, Loss PPS, PER (%)\n')
        for i in range(len(numPktsPerSec)):
            outputFile.write('%d, %d, %d, %f\n' %(i + 1, numPktsPerSec[i], pktLossPerSec[i], PER[i]))
packetStats()

############## COMMANDS
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
