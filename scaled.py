import sys
from sklearn import preprocessing
import pandas as pd

file=sys.argv[1]
df=pd.read_csv(file, sep=',')
df['Close']= preprocessing.scale(df['Close'])
df['Volume']= preprocessing.scale(df['Volume'])
df['changedClose']= preprocessing.scale(df['Close'])
df['changedVolume']= preprocessing.scale(df['changedVolume'])
df['accVolume']= preprocessing.scale(df['accVolume'])
file=str.split(file,'.')[0]
df.to_csv(file+'-scaled.csv', sep=',',index = False)