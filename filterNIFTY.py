import pandas as pd
df=pd.read_csv('INFY_18_1_2017.csv', sep='|')
newdf=pd.DataFrame(df, columns=['lastUpdateTime','lastPrice','quantityTraded'])
newdf.to_csv('INFY_18_1_2017-filter.csv', sep='|')