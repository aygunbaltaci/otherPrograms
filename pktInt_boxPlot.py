#!/usr/bin/env python3

#####################################################
# 04.06.2020
#
# This code extracts the data for the required height
# value from the input file
# 
# Provide your input data:  
# inputfiles/input_extractdata.csv 
# 
# Prerequisites: 
# pip3 install matplotlib csv numpy pandas 
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

import pandas as pd
from datetime import datetime
import csv
import numpy as np

# Variables
inputDir = 'inputfiles'
inputFileName = 'input_extractdata.csv'
outputDir = 'outputfiles'
outputFileName = 'output_extractdata.csv'
height = 50 # provide 0, 10, 20, 30, 40 or 50
currDate = datetime.now().strftime('%Y%m%d_%H%M%S')
# Fetch data and drop NaNs
data = pd.read_csv(inputDir + os.sep + inputFileName)
data2 = data.dropna()

#for i in height:
outputdata = []
outputdata.append(str(height) + 'm')
for j in range(len(data2.iloc[:, 1])):
    if data2.iloc[j, 1] == height:
        outputdata.append(data2.iloc[j, 0])  
outputdata = pd.DataFrame(outputdata)
outputdata.to_csv(outputDir + os.sep + currDate + '_' + outputFileName, mode = 'a', index = False, header = False)