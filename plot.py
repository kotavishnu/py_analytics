import matplotlib.pyplot as plt
import sys
import pandas as pd

file=sys.argv[1]
df=pd.read_csv(file, sep=',')
plt.plot(df['Close'])
plt.plot(df['changedVolume'])

file=str.split(file,'.')[0]
plt.savefig(file+'.png')