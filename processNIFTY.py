import matplotlib.pylab as plt
from sklearn import preprocessing
import pandas as pd
df=pd.read_csv('INFY_18_1_2017-filter.csv', sep='|')
df['lastUpdateTime']=pd.to_datetime(df['lastUpdateTime'], format="%d-%b-%Y %H:%M:%S")
df['lastPrice'] = df['lastPrice'].astype('float64')

df['quantityTraded'] = df['quantityTraded'].str.replace(r'[,]', '').astype('int')
#print(df['lastPrice'])
#print(df['quantityTraded'])
df['changedLastPrice']=df['lastPrice'].diff(1)
df['changedLastPrice']=df['changedLastPrice'].fillna(0)
#print(df['changedLastPrice'])
df['changedQuantityTraded']=df['quantityTraded'].diff(1)
df['changedQuantityTraded']=df['changedQuantityTraded'].fillna(0)
#print(df['changedQuantityTraded'])
df.to_csv('INFY_18_1_2017-processed.csv', sep='|')