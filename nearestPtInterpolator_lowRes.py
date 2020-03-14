#!/usr/bin/python3.6

import sys
import os
import csv
import numpy as np
from datetime import datetime

# ============= Variables
fileDate = datetime.now().strftime('%Y%m%d_%H%M%S')
lowResInputFile = 'lowResData.csv'
highResInputFile = 'highResData.csv'
outputFile = '_nearestPtInterpolator_lowRes'
outputFileFormat = '.csv'
inputDir = 'inputCsvFiles'
outputDir = 'logs'
outputFileName = fileDate + outputFile + outputFileFormat
inputFileDelimeter = ','
outputFileDelimeter = ' '
defaultEncoding = 'utf-8-sig'
lowResData = []
highResData = []
concatRow = []
headerRow = []

# ============= Nearest Point Interpolator
def lookupNearest(x0): # taken from https://stackoverflow.com/questions/31734471/2d-nearest-neighbor-interpolation-in-python
    xi = np.abs(highResData[0] - x0).argmin() # xi is the row number of the closest value in highResData[0] to x0 
    return xi
    
# ============= Fetch low resolution data
with open(inputDir + os.sep + lowResInputFile, 'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = inputFileDelimeter)
    
    # Fetch the lowResData from each row
    for row in plots:
        lowResData.append(row)
    
    lowResData = list(map(list, zip(*lowResData))) # transpose the lowResData: rows -> columns
    
    # Update default label names if labels are given in the input file
    if not (lowResData[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
        for i in range(len(lowResData)): # Delete labels
            headerRow.append(lowResData[i][0])
            del lowResData[i][0]
    
    # Convert input lowResData to float  
    for i in range(len(lowResData)): # iterate over each column    
        lowResData[i] = list(map(float, lowResData[i]))  # convert lowResData to float

# ============= Fetch high resolution data
with open(inputDir + os.sep + highResInputFile,'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = inputFileDelimeter)
    
    # Fetch the high resolution data from each row
    for row in plots:
        highResData.append(row)
    
    highResData = list(map(list, zip(*highResData))) # transpose the lowResData: rows -> columns
    
    # Update default label names if labels are given in the input file
    if not (highResData[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same        
        for i in range(len(highResData)): # Delete labels
            headerRow.append(highResData[i][0])
            del highResData[i][0]
    
    # Convert input highResData to float  
    for i in range(len(highResData)): # iterate over each column    
        highResData[i] = list(map(float, highResData[i]))  # convert lowResData to float
        
# Convert input data to numpy array type
lowResData = np.array(lowResData)
highResData = np.array(highResData)

# ============= Concatenate Interpolated Data
spamWriter = csv.writer(open(outputDir + os.sep + outputFileName, 'w', newline = ''), delimiter = outputFileDelimeter) # Open csv file to write output
spamWriter.writerow(headerRow) # write the header
for i in range(0, len(lowResData[0])): # 0 is the col number in lowResData file
    value = lookupNearest(lowResData[0][i]) # find the row for nearest point interpolation
    for j in range(len(lowResData)):
        concatRow.append(lowResData[j][i])
        # print("GPS DATA: %s" %lowResData[j][i])
    for j in range(len(highResData)):
        # print("PCAP DATA: %s" %highResData[j][value])
        concatRow.append(highResData[j][value])
    # print("concatRow: %s\n\n\n", concatRow)
    spamWriter.writerow(concatRow)
    concatRow = []   
#print("input = %f, outcome = %f" %(lowResData[1][i], value))