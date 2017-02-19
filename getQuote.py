import time
import datetime
import sys
import json
now = datetime.datetime.now()
fileName="INFY_%d_%d_%d"% (now.day,now.month,now.year) +".csv"

print ("date time "+str(now.hour))
from urllib2 import Request, urlopen  # Python 2


q = Request('https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol=INFY&series=EQ')

q.add_header('X-Requested-With', 'XMLHttpRequest')
q.add_header('Cookie', 'pointer=1; sym1=INFY')
q.add_header('Host', 'www.nseindia.com')
q.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
q.add_header('Content-Type', 'text/html;charset=ISO-8859-1')
q.add_header('Referer', 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY')
q.add_header('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
f = open(fileName, 'a')
try:
    header= "lastUpdateTime|open|lastPrice|quantityTraded|percentChange|averagePrice|dayLow|dayHigh"
    f.write(header)

    while(1):
        print("hour "+str(now.hour)+" time is "+str(now.minute))
        if (now.hour >= 10 ):
            sys.exit()
        if now.hour < 3 or (now.hour==3 and now.minute<45):
            print("Waiting.....")
            time.sleep(300)

        a = urlopen(q).read()
        print(a)
        data = json.loads(a.decode("utf-8"))
        print ("data "+str(data))
        line = data['lastUpdateTime'] + "|" + data['data'][0]['open'] + "|" + data['data'][0]['lastPrice'] + "|" + \
               data['data'][0]['totalTradedVolume'] + "|" + data['data'][0]['pChange'] + "|" + data['data'][0][
                   'averagePrice'] + "|" + data['data'][0][
                   'dayLow'] + "|" + data['data'][0]['dayHigh']
        print("Line " + line)
        f.write("\n" + line)
        f.flush()
        f.flush()
        print ("Waiting.....")
        time.sleep(300)
finally:
    print ("Before exit")
    f.flush()
    f.close()