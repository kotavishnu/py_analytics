import matplotlib.pylab as plt
from sklearn import preprocessing
import pandas as pd
import numpy as np
df=pd.read_csv('filter.csv', sep=',')
df['Date']=pd.to_datetime(df['Date'], format="%Y-%m-%d")
df=df.iloc[::-1]
print(df['Date'])
print(df['Close'])
print(df['Volume'])

df = pd.DataFrame(np.random.randn(1000, 4), index=df.index, columns=list('ABC'))
df = df.cumsum()
plt.figure(); df.plot();
plt.show()