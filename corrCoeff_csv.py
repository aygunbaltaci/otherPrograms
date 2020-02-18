#!/usr/bin/python3.6

import os
import csv
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# ============= Variables
fileDate = datetime.now().strftime('%Y%m%d_%H%M%S_')
inputFile = 'corrCoeff.csv'
outputFile = 'corrCoeff_output'
outputFileFormat = '.csv'
outputImgFormat = '.pdf'
inputDir = 'inputCsvFiles'
outputDir = 'logs'
outputFileName = fileDate + outputFile + outputFileFormat
outputImgName = fileDate + outputFile + outputImgFormat
inputFileDelimeter = ','
outputFileDelimeter = ' '
defaultEncoding = 'utf-8-sig'
headerRow = []
inputData = []
outputData = []
meanVal = []
stdVal = []
correlations = []
    
# ============= Fetch GPS Input Data
inputData = pd.read_csv(inputDir + os.sep + inputFile)
f = plt.figure(figsize=(19, 15))
correlations = inputData.corr()
print(correlations)
correlations.to_csv(outputDir + os.sep + outputFileName)
plt.matshow(inputData.corr(), fignum=f.number, cmap = 'twilight_shifted')
plt.xticks(range(inputData.shape[1]), inputData.columns, fontsize=40, rotation=60)
plt.yticks(range(inputData.shape[1]), inputData.columns, fontsize=40)
plt.colorbar()
f.savefig(outputDir+ os.sep + outputImgName, bbox_inches = 'tight', pad_inches = 0)
plt.show()