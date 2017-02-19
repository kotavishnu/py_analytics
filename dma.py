import csv
with open('DMA12-FEB-2017.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        price=float(row['Current Price'])
        if(price >100 and price > float(row['30 Days']) and price > float(row['50 Days']) and price > float(row['150 Days']) and price > float(row['200 Days'])):
            print(row['Company Name']+','+ row['Current Price']+','+row['Change %']+','+ row['30 Days']+','+row['50 Days']+','+ row['150 Days']+','+ row['200 Days'])
