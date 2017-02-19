import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen  # Python 3
stocks=['ABB','APOLLOHOSP','ASHOKLEY','BAJFINANCE','BAJAJFINSV','BEL','BHARATFORG','BRITANNIA','CADILAHC','CASTROLIND','COLPAL','CONCOR','CUMMINSIND','DLF','DABUR','DIVISLAB','EMAMILTD','GSKCONS','GLAXO','GLENMARK','GODREJCP','HAVELLS','HINDPETRO','HINDZINC','IBULHSGFIN','IOC','INDIGO','JSWSTEEL','LICHSGFIN','MARICO','MOTHERSUMI','NHPC','NMDC','OIL','OFSS','PIDILITIND','PEL','PFC','PGHH','PNB','SHREECEM','SRTRANSFIN','SIEMENS','SAIL','TITAN','TORNTPHARM','UPL','UBL','MCDOWELL-N','VEDL']
for stk in stocks:

    q = Request('https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol='+stk+'&segmentLink=3&symbolCount=2&series=ALL&dateRange=1month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE')
    q.add_header('X-Requested-With', 'XMLHttpRequest')
    q.add_header('Cookie', 'pointer=1; sym1=INFY')
    q.add_header('Host', 'www.nseindia.com')
    q.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    q.add_header('Content-Type', 'text/html;charset=ISO-8859-1')
    q.add_header('Referer', 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY')
    q.add_header('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')

    a = urlopen(q).read()

    soup = BeautifulSoup(a)

    table = soup.find_all('table')[0]
    rows = table.find_all('tr')[1:]
    data = {
        'vol' : []
    }
    for row in rows:
        cols = row.find_all('td')
        data['vol'].append(cols[10].get_text())
    df= pd.DataFrame( data )
    df['vol'] = df['vol'].str.replace(r'[,]', '').astype('float64')
    print(stk+','+str(df['vol'].mean()))