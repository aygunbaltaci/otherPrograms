#!/usr/bin/env python3

#####################################################
# 04.06.2020
#
# This code generates the PDF distribution of given
# data and matches it to a best fitting continuous
# distribution:
# 
# Provide your input data:  
# inputfiles/input_fit_distribution.csv
# 
# Prerequisites: 
# pip3 install matplotlib numpy pandas scipy 
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

######################## MAIN CODE TAKEN FROM: https://stackoverflow.com/questions/6620471/fitting-empirical-distribution-to-theoretical-ones-with-scipy-python?lq=1

import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib
import matplotlib.pyplot as plt
import time
from datetime import datetime

matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')
currDate = datetime.now().strftime('%Y%m%d_%H%M%S')
inputDir = 'inputfiles'
inputFileName = "input_fit_distribution.csv"
outputDir = 'outputfiles'
outputFileName = "output_fit_distribution.csv"

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    startTime = time.time()
    time1 = []
    time2 = []
    allSSE = []
    allParams = []
    loopCnt = 0

    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

     # Continuous distribution models from scipy stats: https://docs.scipy.org/doc/scipy/reference/stats.html
    DISTRIBUTIONS = [        
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]
    
    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf
    
    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:
        time1.append(time.time())

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
                allSSE.append(sse)
                allParams.append(params)
                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass
        
        loopCnt += 1
        time2.append(time.time())
        print(np.mean(time2))
        
        print("""\n\n\n
        DISTRIBUTION: %s
        %d out of %d completed (%f%%). 
        Loop time: %f, total elapsed time: %f 
        Estimated leftover time: %f""" 
       %(distribution, loopCnt, len(DISTRIBUTIONS), (loopCnt/len(DISTRIBUTIONS)) * 100,
        time2[-1] - time1[-1], time2[-1] - startTime, (np.mean(time2) - np.mean(time1)) * (len(DISTRIBUTIONS) - loopCnt)))
    
    print(len(DISTRIBUTIONS), len(allSSE), len(allParams))    
    # Save data to an output file
    outputData = np.column_stack((DISTRIBUTIONS, allSSE, allParams))
    outputData = pd.DataFrame(outputData, columns = ['dist type', 'sse', 'params'])
    print(outputData)
    outputData = outputData.sort_values('sse')
    print(outputData)
    outputData.to_csv(outputDir + os.sep + currDate + outputFileName, sep = ',')

    return (best_distribution.name, best_params, best_sse)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

# Load data from statsmodels datasets
allData = pd.read_csv(inputDir + os.sep + inputFileName)
allData2 = allData.dropna()
data = allData2['Data Rate (kbps)_spark_ul']

# Plot for comparison
plt.figure(figsize=(12,8))
ax = data.plot(kind='hist', bins=50, normed=True, alpha=0.5)
# Save plot limits
dataYLim = ax.get_ylim()

# Find best fit distribution
best_fit_name, best_fit_params, sse = best_fit_distribution(data, 200, ax)
best_dist = getattr(st, best_fit_name)

# Update plots
ax.set_ylim(dataYLim)
ax.set_title('All Fitted Distributions')
ax.set_xlabel('Data Rate (kbps)2')
ax.set_ylabel('Frequency')

# Make PDF with best params 
pdf = make_pdf(best_dist, best_fit_params)

# Display
plt.figure(figsize=(12,8))
ax = pdf.plot(lw=2, label='PDF', legend=True)
data.plot(kind='hist', bins=50, normed=True, alpha=0.5, label='Data', legend=True, ax=ax)
print("sse: %f" %sse)
param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
dist_str = '{}({}){}'.format(best_fit_name, param_str, sse)

ax.set_title('Best fit distribution \n' + dist_str)
ax.set_xlabel('Data Rate (kbps)')
ax.set_ylabel('Frequency')

plt.show()