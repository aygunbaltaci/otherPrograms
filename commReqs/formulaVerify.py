import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as st
import scapy 
import pandas as pd
import math 
from scipy import constants
from datetime import datetime
import config_optional

plt.rcParams.update(config_optional.parameters)

# Variables
inputData2 = pd.read_csv('formulaVerify_spark.csv')
inputData = inputData2.dropna()
scenario = 'ul' # select 'dl' or 'ul'
title = ['Downlink', 'Uplink']
figSize = (25.6, 14.4)
currDate = datetime.now().strftime('%Y%m%d_%H%M%S')
numSamples = 100000
numBins = 50
lineWidth = 2
lineOpacity = 0.5
N = len(inputData.iloc[:,0]) # num of packets
Ptx = 18 # tx power
Gtx = 0 # tx gain
Grx = 0 # rx gain
alpha = 2.2 # PE
#d = inputData['Distance (m)'] # np.random.uniform(0.183, 23.36, N) # comm distance
#v = inputData['Speed (m/s)']
Pn = -101 # noise floor
f = 2.4 * 10 ** 8 # comm freq
c = 3 * 10 ** 8 # speed of light
prevSpeed = 0
Rt, sse, mean, std, origMean, origStd = [], [], [], [], [], []

fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = figSize)

if scenario == 'dl':   
    Dt = 10 # color depth of camera
    Ft = 60 # fps
    Xt = 0.95 # compression rate

for j in range(2):
    if j == 0: # dl 
        for i in range(N):
            Ct = Ptx + Gtx + Grx - (10 * alpha * np.log10((4 * math.pi * inputData.iloc[i]['Distance (m)'] * f) / c)) > Pn
            #print(Ptx + Gtx + Grx - (10 * alpha * np.log10((4 * math.pi * inputData.iloc[i]['Distance (m)'] * f) / constants.speed_of_light)))
            Nt = np.random.uniform(9.9, 10) * (np.absolute((inputData.iloc[i]['Speed (m/s)'] - prevSpeed)*0.1) + 0.1) # num of pixels
            Ltel_t = inputData.iloc[i]['avg_Packet Length (bytes)']
            Btel_t = 1 / (inputData.iloc[i]['avg_Packet Interval (ms)'] / 1000) # 1000 to convert into s and 1 / division to convert into Hz
            Lvideo_t = inputData.iloc[i]['avg_Packet Length (bytes)2']
            Bvideo_t = 1 / (inputData.iloc[i]['avg_Packet Interval (ms)2'] / 1000) # 1000 to convert into s and 1 / division to convert into Hz
            print(Bvideo_t)
            Rt.append((Ltel_t * Btel_t + Lvideo_t * Bvideo_t) * 8 / 1000 * Ct) # 8 * to convert bytes to bits, 1000 to convert bps to kbps
            prevSpeed = inputData.iloc[i]['Speed (m/s)']
    else: # ul
        for i in range(N):
            Ct = Ptx + Gtx + Grx - (10 * alpha * np.log10((4 * math.pi * inputData.iloc[i]['Distance (m)2'] * f) / c)) > Pn
            #print(Ptx + Gtx + Grx - (10 * alpha * np.log10((4 * math.pi * inputData.iloc[i]['Distance (m)'] * f) / constants.speed_of_light)))
            Lcnt = 1 / (inputData.iloc[i]['avg_Packet Interval (ms)3'] / 1000) # 1000 to convert into s and 1 / division to convert into Hz
            Bcnt = inputData.iloc[i]['avg_Packet Length (bytes)3']
            Rt.append(Lcnt * Bcnt * 8 / 1000 * Ct) # 8 * to convert bytes to bits, 1000 to convert bps to kbps

    # Calculate mean and std of original data
    origMean.append(np.mean(Rt))
    origStd.append(np.std(Rt))
    
    # Fit original data to normal distribution
    params = st.norm.fit(Rt)
    
    # Separate parts of parameters of normal distribution
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    
    # Fetch hist (y2) and bin edge (x2) values of original data
    y2, x2 = np.histogram(Rt, bins = numSamples, density = True)
    x2 = (x2 + np.roll(x2, -1))[:-1] / 2.0

    # Get start and end points of distribution
    start = st.norm.ppf(0.00001, *arg, loc = loc, scale = scale) if arg else st.norm.ppf(0.00001, loc = loc, scale = scale)
    end = st.norm.ppf(0.99999, *arg, loc = loc, scale = scale) if arg else st.norm.ppf(0.99999, loc = loc, scale = scale)

    # Build bimodal PDF
    size = numSamples
    x = np.linspace(start, end, size)
    y = st.norm.pdf(x, loc = loc , scale = scale , *arg) # st.norm.pdf(x, loc = loc + (scale * rightPeak_xShift[i]), scale = scale / rightPeak_yShift[i], *arg) + st.norm.pdf(x, loc = loc - (scale * leftPeak_xShift[i]), scale = scale / leftPeak_yShift[i], *arg)
    
    # Calculate pdf, mean and std
    pdf = pd.Series(y, x)
    mean.append(loc)
    std.append(scale)
    
    # Calculate SSE
    sse.append(np.sum(np.power(y2 - y, 2.0)))

    # remove the empty plot on the right column
    ax[j, 1].remove()

    # Plot the data
    ax[j, 0].hist(Rt, bins = numBins, density = True, color = 'steelblue', alpha = lineOpacity, label = 'PDF of Generated Data \n ($\mu$ = %.2f, $\sigma$ = %.2f)' %(origMean[-1], origStd[-1]))
    ax[j, 0].plot(pdf, lw = lineWidth, color = 'sandybrown', lineStyle = '--', alpha = lineOpacity, label = 'Distribution Model \n ($\mu$ = %.2f, $\sigma$ = %.2f, SSE = %.2f)' %(mean[-1], std[-1], sse[-1]))
    ax[j, 0].spines['top'].set_visible(False)
    leg = ax[j, 0].legend()
    ax[j, 0].set_xlabel('Data Rate (kbps)')
    ax[j, 0].set_ylabel('Frequency')
    ax[j, 0].set_title(title[j])
    Rt = []
    
fig.savefig('%s.%s' %(currDate, 'pdf'), bbox_inches = 'tight', format = 'pdf')
plt.show()