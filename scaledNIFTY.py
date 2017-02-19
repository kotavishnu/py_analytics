import matplotlib.pyplot as plt
import matplotlib as mat
from sklearn import preprocessing
import pandas as pd
df=pd.read_csv('INFY_18_1_2017-processed.csv', sep='|')
df['lastPrice'] = preprocessing.scale(df['lastPrice'])
df['quantityTraded']= preprocessing.scale(df['quantityTraded'])
df['changedLastPrice'] = preprocessing.scale(df['changedLastPrice'])
df['changedQuantityTraded']= preprocessing.scale(df['changedQuantityTraded'])
df.to_csv('INFY_18_1_2017-scaled.csv', sep='|')