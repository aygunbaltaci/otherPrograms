import numpy as np
import csv
from numpy import genfromtxt
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import mean_squared_error
from scipy.stats import ranksums


samples = genfromtxt('pktlen_ul_real.csv', delimiter=',')
samples2 = genfromtxt('pktlen_ul_sim.csv', delimiter=',')

############# METHOD 1 - MSE 
bins = np.linspace(0, 1550, 1550)
pdf = []

for i in [samples, samples2]:
    histogram, bins = np.histogram(i, bins=bins, density=True)
    #print(bins)
    bin_centers = 0.5*(bins[1:] + bins[:-1])

    # Compute the PDF on the bin centers from scipy distribution object
    pdf.append(histogram)
    
print(pdf)
mse = mean_squared_error(pdf[0], pdf[1]) # 0: true, 1: simulation
print("mse: %.10f" %mse) 
np.savetxt("pktlen_ul_pdf.csv", pdf, delimiter=",")

############# METHOD 2 - Wilcoxon rank sum test
#statistics, p = ranksums(samples, samples2)

############# METHOD 3 - Kolmogorov-Smirnov statistics
#statistics, p = stats.ks_2samp(samples, samples2)

############# METHOD 4 - Epps-Singleton statistics
#statistics, p = stats.epps_singleton_2samp(samples, samples2)

#print("statistics: %.15f" %statistics)
#print("p: %.15f" %p)