import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

census_data = pd.read_csv("seaborn.csv")

print(census_data.head())

sns.relplot(x='Time (s)',y='Packet Interval (ms)', kind="line", data=census_data)
plt.show()
