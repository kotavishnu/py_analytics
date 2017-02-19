import pandas as pd
import sys
file=sys.argv[1]
print ("file is"+file)
df=pd.read_csv(file, sep=',')
newdf=pd.DataFrame(df, columns=['Date','Close','Volume'])
file=str.split(file,'.')[0]
newdf.to_csv(file+'-filter.csv', sep=',',index = False)