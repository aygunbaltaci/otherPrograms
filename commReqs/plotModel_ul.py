#!/usr/bin/env python3

#####################################################
# 04.06.2020
#
# This code computes the PDF distribution of the 
# given data and fits it to the user-selected 
# distribution. It graphs the result. 
# statistical distribution and graphs the PDF.  
# 
# Provide your input data:
# inputfiles/input_removenans.csv 
# 
# Prerequisites: 
# pip3 install matplotlib numpy pandas scipy
#
# The code fits the given data to a normal distribution.
# If you want to fit to another distribution, change the
# lines in the code: 
# st.norm.* -> st.<selected-distribution-name>.*
#
# The names of the distributions are listed below:
# https://docs.scipy.org/doc/scipy/reference/stats.html
# 
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

import os
import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
from statsmodels.tsa.arima_model import ARMA
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt
import time
import seaborn as sns
import math
from datetime import datetime
import config_optional
plt.rcParams.update(config_optional.parameters) # update matplotlib parameters

# Variables    
rfCh = [1.8, 1, 1.6]
camera = [1, 1, 0.6]
velocity = [1, 1, 1]
numData = 3
numSamples = 100000
lineWidth = 2
lineOpacity = 0.5
numBins = 50
figSize = (25.6, 14.4)
inputDir = 'inputfiles'
inputFileName = 'input_fitdata_toselecteddistribution_ul.csv'
outputDir = 'outputfiles'
outputfileName = 'output_fitdata_toselecteddistribution_ul.csv'
currDate = datetime.now().strftime('%Y%m%d_%H%M%S')
colNames = ['Packet Length (bytes)', 'Packet Length (bytes)2', 'Packet Length (bytes)3']
title = ['DJI Spark', 'DJI Mavic', 'Parrot AR 2.0']
xLabel = 'Packet Length (bytes)'

# Fetch data and drop NaN
allData = pd.read_csv(inputDir + os.sep + inputFileName)
allData2 = allData.dropna()

# Initialize arrays
mean = []
std = []
origMean = []
origStd = []
data = []
sse = []
rightPeak_xShift = []
rightPeak_yShift = []
leftPeak_xShift = []
leftPeak_yShift = []

# Set up shifting and scaling parameters
for i in range(numData):
    data.append(0)
    rightPeak_xShift.append(1 * camera[i])
    rightPeak_yShift.append(1 * rfCh[i] * velocity[i])
    leftPeak_xShift.append(1 * camera[i])
    leftPeak_yShift.append(1 / (rfCh[i] * velocity[i]))
    origMean.append(0)
    origStd.append(0)
    data[i] = allData2[colNames[i]]

# Set up plotting environment
fig, ax = plt.subplots(nrows = len(data), ncols = 2, figsize = figSize)

for i in range(numData):
    
    # Calculate mean and std of original data
    (origMean[i], origStd[i]) = st.norm.fit(data[i])

    # Fit original data to normal distribution
    params = st.norm.fit(data[i])
    
    # Separate parts of parameters of normal distribution
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    
    # Fetch hist (y2) and bin edge (x2) values of original data
    y2, x2 = np.histogram(data[i], bins = numSamples, density = True)
    x2 = (x2 + np.roll(x2, -1))[:-1] / 2.0

    # Get start and end points of distribution
    start = st.norm.ppf(0.00001, *arg, loc = loc, scale = scale) if arg else st.norm.ppf(0.00001, loc = loc, scale = scale)
    end = st.norm.ppf(0.99999, *arg, loc = loc, scale = scale) if arg else st.norm.ppf(0.99999, loc = loc, scale = scale)

    # Build normal PDF
    size = numSamples
    x = np.linspace(start, end, size)
    y = st.norm.pdf(x, loc = loc , scale = scale , *arg)
    print(y.shape)
    
    # Calculate mean and std
    pdf = pd.Series(y, x)
    #print(y.sum())
    mean.append(loc)
    std.append(scale )
    
    # Calculate SSE
    sse.append(np.sum(np.power(y2 - y, 2.0)) / numSamples)
    
    # remove the empty plot on the right column
    ax[i, 1].remove()

    # Plot the data
    ax[i, 0].hist(data[i], bins = numBins, density = True, color = 'steelblue', alpha = lineOpacity, label = 'PDF of Original Data \n ($\mu$ = %.2f, $\sigma$ = %.2f)' %(origMean[i], origStd[i]))
    ax[i, 0].plot(pdf, lw = lineWidth, color = '#ff7f0e', lineStyle = '--', alpha = lineOpacity, label = 'Distribution Model \n ($\mu$ = %.2f, $\sigma$ = %.2f, SSE = %.2f)' %(mean[-1], std[-1], sse[-1]))
    ax[i, 0].spines['top'].set_visible(False)
    leg = ax[i, 0].legend()
    ax[i, 0].set_xlabel(xLabel)
    ax[i, 0].set_ylabel('Frequency')
    ax[i, 0].set_title(title[i]) 

fig.savefig('%s.%s' %(outputDir + os.sep + currDate + '_' + outputFileName, 'pdf'), bbox_inches = 'tight', format = 'pdf')
plt.show()