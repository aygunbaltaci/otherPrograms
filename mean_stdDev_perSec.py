#!/usr/bin/python3.6

import os
import csv
import numpy as np
from datetime import datetime

# ============= Variables
fileDate = datetime.now().strftime('%Y%m%d_%H%M%S_')
inputFile = 'mean_stdDev_input.csv'
outputFile = 'mean_stdDev_output.csv'
outputFileFormat = '.csv'
inputDir = 'inputCsvFiles'
outputDir = 'logs'
outputFileName = fileDate + outputFile + outputFileFormat
inputFileDelimeter = ','
outputFileDelimeter = ' '
defaultEncoding = 'utf-8-sig'
headerRow = []
inputData = []
outputData = []
meanVal = []
stdVal = []
concatRow = []
    
# ============= Fetch GPS Input Data
with open(inputDir + os.sep + inputFile, 'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = inputFileDelimeter)
    
    # Fetch the inputData from each row
    for row in plots:
        inputData.append(row)
    
    inputData = list(map(list, zip(*inputData))) # transpose the inputData: rows -> columns
    numDataGPS = len(inputData)
    
    # Update default label names if labels are given in the input file
    if not (inputData[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
        for i in ['avg_', 'stdDev_']:
            for j in range(numDataGPS): # Write header row
                headerRow.append(i + inputData[j][0])
                
        for j in range(numDataGPS): # Delete labels
                del inputData[j][0]
    # Convert input inputData to float  
    for i in range(numDataGPS): # iterate over each column    
        inputData[i] = list(map(float, inputData[i]))  # convert inputData to float

counterOld = 0
counter = 0
inputCounter = 0
timeOld = int(inputData[0][0])
time = int(inputData[0][0])
meanVal = [[0 for x in range(len(inputData))] for y in range(int(inputData[0][-1]) - int(inputData[0][0]))]  
stdDevVal = [[0 for x in range(len(inputData))] for y in range(int(inputData[0][-1]) - int(inputData[0][0]))] 
#print(len(inputData), len(inputData[0]), meanVal) 
for i in range(len(inputData[0])): # Assuming that the first col is the time col
    time = int(inputData[0][i])
    print(time)
    if time != timeOld:
        print(time, timeOld, i, counterOld, counter, inputCounter)
        for j in range(len(inputData)):
            meanVal[inputCounter][j] = np.mean(inputData[j][counterOld:counter])
            stdDevVal[inputCounter][j] = np.std(inputData[j][counterOld:counter])
        inputCounter += 1
        counterOld = counter
        timeOld = time
    counter += 1
        
# ============= Write Output Data
spamWriter = csv.writer(open(outputDir + os.sep + outputFileName, 'w'), delimiter = outputFileDelimeter) # Open csv file to write output
spamWriter.writerow(headerRow) # write the header
concatenatedData = np.concatenate((meanVal, stdDevVal), axis = 1) # axis = 1 means to concatenate arrays column-wise
spamWriter.writerows(concatenatedData)