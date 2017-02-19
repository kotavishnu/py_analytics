import pandas as pd
import sys
file=sys.argv[1]
df=pd.read_csv(file, sep=',')
df['Date']=pd.to_datetime(df['Date'], format="%Y-%m-%d")
df=df.iloc[::-1]
df['changedClose']=df['Close'].diff(1)
df['changedClose']=df['changedClose'].fillna(0)
df['changedVolume']=df['Volume'].diff(1)
df['changedVolume']=df['changedVolume'].fillna(0)
df['accVolume']=df['changedVolume'].diff(1)
df['accVolume']=df['accVolume'].fillna(0)
file=str.split(file,'.')[0]
df.to_csv(file+'-processed.csv', sep=',',index = False)