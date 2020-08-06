#!/usr/bin/env python

#####################################################
# 04.06.2020
#
# This code removes NaNs from the 1st column of 
# given csv file:  
# inputfiles/input_removenans.csv 
# 
# Prerequisites: 
# pip3 install pandas 
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

import pandas as pd 
from datetime import datetime

# ======== variables
inputDir = 'inputfiles'
inputFileName = 'input_removenans.csv '
outputDir = 'outputfiles'
outputFileName = 'output_removenans.csv '
date = datetime.now().strftime('%Y%m%d_%H%M%S')

data = pd.read_csv(inputDir + os.sep + inputFileName)

print(data)
data2 = data.dropna()
print(data2)

data2.to_csv(outputDir + os.sep + date + '_' + outputFileName)
