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
outputFile = '_nearestPtInterpolator'
outputFileFormat = '.csv'
inputDir = 'inputCsvFiles'
outputDir = 'logs'
outputFileName = fileDate + outputFile + outputFileFormat
inputFileDelimeter = ','
outputFileDelimeter = ' '
defaultEncoding = 'utf-8-sig'
inputLowResData = []
inputHighResData = []
concatRow = []
headerRow = []

# ============= Nearest Point Interpolator
def lookupNearest(x0): # taken from https://stackoverflow.com/questions/31734471/2d-nearest-neighbor-interpolation-in-python
    xi = np.abs(inputHighResData[0] - x0).argmin() # xi is the row number of the closest value in inputHighResData[0] to x0 
    return xi
    
# ============= Fetch low resolution data
with open(inputDir + os.sep + lowResInputFile, 'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = inputFileDelimeter)
    
    # Fetch the inputLowResData from each row
    for row in plots:
        inputLowResData.append(row)
    
    inputLowResData = list(map(list, zip(*inputLowResData))) # transpose the inputLowResData: rows -> columns
    
    # Update default label names if labels are given in the input file
    if not (inputLowResData[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
        for i in range(len(inputLowResData)): # Delete labels
            headerRow.append(inputLowResData[i][0])
            del inputLowResData[i][0]
    
    # Convert input inputLowResData to float  
    for i in range(len(inputLowResData)): # iterate over each column    
        inputLowResData[i] = list(map(float, inputLowResData[i]))  # convert inputLowResData to float

# ============= Fetch high resolution data
with open(inputDir + os.sep + highResInputFile,'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = inputFileDelimeter)
    
    # Fetch the high resolution data from each row
    for row in plots:
        inputHighResData.append(row)
    
    inputHighResData = list(map(list, zip(*inputHighResData))) # transpose the inputLowResData: rows -> columns
    
    # Update default label names if labels are given in the input file
    if not (inputHighResData[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same        
        for i in range(len(inputHighResData)): # Delete labels
            headerRow.append(inputHighResData[i][0])
            del inputHighResData[i][0]
    
    # Convert input inputHighResData to float  
    for i in range(len(inputHighResData)): # iterate over each column    
        inputHighResData[i] = list(map(float, inputHighResData[i]))  # convert inputLowResData to float
        
# Convert input data to numpy array type
inputLowResData = np.array(inputLowResData)
inputHighResData = np.array(inputHighResData)

# ============= Concatenate Interpolated Data
spamWriter = csv.writer(open(outputDir + os.sep + outputFileName, 'w', newline = ''), delimiter = outputFileDelimeter) # Open csv file to write output
spamWriter.writerow(headerRow) # write the header
for i in range(0, len(inputLowResData[0])): # 0 is the col number in lowResData file
    value = lookupNearest(inputLowResData[0][i]) # find the row for nearest point interpolation
    for j in range(len(inputLowResData)):
        concatRow.append(inputLowResData[j][i])
        # print("GPS DATA: %s" %inputLowResData[j][i])
    for j in range(len(inputHighResData)):
        # print("PCAP DATA: %s" %inputHighResData[j][value])
        concatRow.append(inputHighResData[j][value])
    # print("concatRow: %s\n\n\n", concatRow)
    spamWriter.writerow(concatRow)
    concatRow = []   
#print("input = %f, outcome = %f" %(inputLowResData[1][i], value))