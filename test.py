#!/usr/bin/env python3

import seaborn as sns 
import pandas as pd
import matplotlib.pyplot as plt
import csv 
from datetime import datetime
#sns.set(style="ticks")
dateNow = datetime.now().strftime('%Y%m%d_%H%M%S')
# Load the example dataset for Anscombe's quartet
df = pd.read_csv('latency.csv')
#pd.Series(df).to_frame()
#with open('plotFromCsv.csv', 'r', encoding = 'utf-8-sig') as csvfile: 
#    df = csv.reader(csvfile, delimiter = ',')
            
#print(df)
# Show the results of a linear regression within each dataset
#sns.scatterplot(x=df.iloc[:, 0], y=df.iloc[:, 2], hue=df.iloc[:, 2]) #col=2, hue=3, data=df,
#for col in df.columns: 
#    print(col) 
#sns.lineplot(x="Time (s)", y="Packet Interval (ms)", ci="sd", data=df)
#sns.lineplot(x=df.iloc[:, 0], y=df.iloc[:, 3], data=df)
#sns.distplot(df.iloc[:, 2], bins=100, kde= True)#, hue=df.iloc[:, 2]) #col=2, hue=3, data=df,
#sns.countplot(df.iloc[:, 2])
#sns.boxplot( df.iloc[:, 1])
           #col_wrap=2, ci=None, palette="muted", height=4,
           #scatter_kws={"s": 50, "alpha": 1})
#sns.scatterplot(x=df.iloc[:, 0], y=df.iloc[:, 1])#,


#fmri = sns.load_dataset("fmri")
#print(fmri)
fig = plt.figure(figsize = (19.2, 10.8))
ax = plt.subplot(3, 2, 1)
sns.lineplot(x="Packet Length (Bytes)", y="Latency (ms)", data=df, markers = True)
sns.lineplot(x="Packet Length (Bytes)", y="Latency (ms)2", data=df, markers = True)
#sns.lineplot(x="Time (s)19", y="Data Rate (kbps)19", data=df, markers = True)
#plt.ylim(0, 200)
ax.set_xlabel("Packet Length (bytes)", size = 15)
ax.set_ylabel("Latency (ms)", size = 15)
plt.legend(labels=['Link 1', 'Link 2'])
ax.set_title('Latency on Downlink Channel', fontdict={'fontsize': 18, 'fontweight': 'medium'})
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

ax2= plt.subplot(3, 2, 3)
sns.lineplot(x="Packet Length (Bytes)", y="Latency (ms)", data=df, markers = True)
#sns.lineplot(x="Time (s)33", y=" PER (%)34", data=df, markers = True)
#sns.lineplot(x="Time (s)24", y="Data Rate (kbps)24", data=df, markers = True)
#sns.regplot(x="Time (s)555", y="Packet Interval (ms)555", data=df, order=2)
#ax.legend(handles=ax.lines[::len(df)+1], labels=["A","B"])
ax2.set_xlabel("Time (s)", size = 15)
ax2.set_ylabel("PER (%)", size = 15)
plt.legend(labels=['Link 1', 'Link 2'])
ax2.set_title('Uplink', fontdict={'fontsize': 18, 'fontweight': 'medium'})
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

ax3= plt.subplot(3, 2, 5)
#kwargs = {'cumulative': True}
#sns.kdeplot(df.iloc[:, 2], hist_kws=kwargs, kde_kws=kwargs)
sns.kdeplot(df["Latency (ms)"], cumulative = True)
sns.kdeplot(df["Packet Length (Bytes)"], cumulative = True)
plt.xlabel('xlabel')
plt.ylabel('ylabel')
plt.xlim(1e+0, 1e+3)
ax3.set_xscale('log')

plt.legend(labels=['legendEntry1', 'legendEntry2'])

#sns.regplot(x="x", y="f", data=df1, order=2, ax=ax)
#sns.regplot(x="x", y="g", data=df2, order=2, ax=ax2)
fig.subplots_adjust(hspace=0.5)
fig.savefig('pktInt_dl_%s.png' %dateNow, bbox_inches = 'tight', format = 'pdf', dpi = 100)
plt.show()