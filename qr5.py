import time
import json
import pandas as pd
import numpy as np
from pandas import DataFrame
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
import smtplib
import datetime
import urllib
from collections import deque
try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2

avgVolArr = {'symbol': ['TCS','INFY','YESBANK','POWERGRID','ONGC','ZEEL','VEDL','SBIN','TATAMOTORS','TECHM','JSWSTEEL','SUNPHARMA','IOC','ICICIBANK','BPCL','NTPC','GAIL','INFRATEL','RELIANCE','LT','EICHERMOT','BHARTIARTL','ITC','BAJAJFINSV','WIPRO','ASIANPAINT','ADANIPORTS','BAJAJ-AUTO','AXISBANK','BAJFINANCE','CIPLA','COALINDIA','DRREDDY','GRASIM','HCLTECH','HDFC','HDFCBANK','HEROMOTOCO','HINDALCO','HINDPETRO','HINDUNILVR','IBULHSGFIN','INDUSINDBK','KOTAKBANK','M&M','MARUTI','TATASTEEL','TITAN','UPL','ULTRACEMCO'],
                 'avgVol':
                  ['30.29314','89.83359','523.18831','63.50447','145.0074','115.75682','102.54123','257.64217','279.37722','28.02312','67.57401','61.44055','150.63734','183.70264','63.54631','154.45219','45.6983','31.55231','98.93051','30.72363','1.21738','90.17462','119.68825','2.19229','78.11553','13.38353','38.93604','5.56481','82.13998','14.66676','25.28549','96.32937','7.4296','15.97825','22.14731','33.8591','36.64808','7.73116','75.14138','77.54994','14.57471','98.92198','35.1409','28.62197','31.23381','9.28579','92.63711','21.30982','17.59486','5.6886']}
def getSummary(data,prev_nifty):
    advances = data['advances']
    declines = data['declines']
    ltp = data['latestData'][0]['ltp']
    ch = data['latestData'][0]['ch']
    icurr=iprev=0
    try:
        icurr=float(ch)
        iprev=float(prev_nifty)
    except Exception as e:
        traceback.print_exc()
        print(str(e))
    change=round(icurr-iprev,2)
    print("Diff from last change is ",change)
    special_alert=''
    if change >10 or change <-10:
        special_alert='Special Alert '+str(change)+' ,'
    ch = data['latestData'][0]['ch']
    per = data['latestData'][0]['per']
    pdat = special_alert+"NIFTY :" + str(ltp) + " " + ch + " " + per + "% diff is "+str(change)
    return pdat
def header(df,lstUpdateTime,summary):
    gainers = df.loc[(df['per'] > 0)]
    loosers = df.loc[(df['per'] <= 0)]
    html = formatHeader(gainers, loosers, lstUpdateTime, summary)
    return html
def formatHeader(gainers, loosers, lstUpdateTime, summary,gainersChangeLen=0,loosersChangeLen=0):
    advances = data['advances']
    declines = data['declines']
    ltp = data['latestData'][0]['ltp']
    ch = data['latestData'][0]['ch']
    per = data['latestData'][0]['per']
    gainersLen = len(gainers.axes[0])
    loosersLen = len(loosers.axes[0])
    print("Advances " + str(gainersLen) + " Loosers " + str(gainersLen))
    html = '<br>NSE Time ' + lstUpdateTime + ' ' + summary
    html += '<table border="1" class="dataframe"><tr><td>&nbsp;</td><td>Advance</td><td>Declines</td><td><tr><td>NIFTY</td><td>' + str(advances) + '</td><td>' + str(declines) + '</td></tr>'
    html += '<tr><td>Filtered</td><td>' + str(gainersLen) + '</td><td>' + str(loosersLen) + '</td></tr>'
    html += '<tr><td>Filtered  Price Percentchange</td><td>' + str(gainersChangeLen) + '</td><td>' + str(loosersChangeLen) + '</td></tr>'
    html += '<tr><td>Anomoly Gainers and loosers </td><td>' + str(gainersLen - loosersLen) + '</td><td>&nbsp;</td></tr>'
    html += '<tr><td>Anomoly Change in price in 9 mins</td><td>' + str(gainersChangeLen - loosersChangeLen) + '</td><td>&nbsp;</td></tr>'
    html += '<tr><td>Anomoly Nifty</td><td>' + str(advances - declines) + '</td><td>&nbsp;</td></tr>'
    html += '</table'
    return html
def perProcessing(sdf,lstUpdateTime,avgVolDF):
    sdf = pd.merge(sdf, avgVolDF, on='symbol', how='inner')
    sdf['time']=lstUpdateTime
    print(sdf.head())
   # print('Merged with AVG'+sdf)
    sdf = sdf.loc[:, ['symbol', 'ltP', 'per', 'trdVol','avgVol','high','low','time','mVal'], ]
    sdf.trdVol = sdf.trdVol.str.replace(',','')
    sdf.per = sdf.per.str.replace(',', '')
    sdf.time = lstUpdateTime
    sdf.ltP = sdf.ltP.str.replace(',', '')
    sdf.low = sdf.low.str.replace(',', '')
    sdf.high = sdf.high.str.replace(',', '')
    sdf.trdVol = sdf.trdVol.astype(float).fillna(0.0)
    sdf.per = sdf.per.astype(float).fillna(0.0)
    sdf=sdf.apply(pd.to_numeric,errors='ignore')

    sdf['avgVolTms'] = sdf['trdVol'] / sdf['avgVol']
    sdf['higherhigh']=((sdf.high-sdf.ltP))/sdf.ltP
    sdf['lowerlow'] = ((sdf.ltP - sdf.low) ) / sdf.low
    sdf=set_rank(sdf)
    sdf = sdf.round(3)
    return sdf
def filter_stocks(sdf):
    sdf = sdf.query('avgVolTms > 0.05')
    #sdf = sdf.query('ltP > 300')
    sdf = sdf.sort_values(by=['avgVolTms'], ascending=[0])
    sdf=set_rank(sdf)
    return sdf
def outlook(sub,body):
    user = "xxxx@xxxx.com"
    pass1 = "xx$321"#"xxx$321"
    try:
        try:
            server = smtplib.SMTP('smtp-mail.xxxx.com', 587)
        except Exception as e:
            print(e)
            server = smtplib.SMTP_SSL('smtp-mail.xxx.com', 465)

        server.set_debuglevel(0)
        server.ehlo()
        server.starttls()
        server.login(user, pass1)
        now = datetime.datetime.now()
        strg = now.strftime('%Y-%m-%d %H:%M:%S%z')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sub
        msg['From'] = user
        msg['To'] = user
        body = "Curr time " + strg + "\n\r" + body
        part2 = MIMEText(body, 'html')
        msg.attach(part2)
        #print("message is " + body)
        server.sendmail("xxx@xxx.com", "xx.xx@xxx.com", msg.as_string())
        server.quit()
        print("Sent message successfully outlook")
    except Exception as e:
        #sendmail1(sub,body)
        print('Something went wrong...' + str(e))
def getQuote(stk):
    q = Request(
        'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol=' + stk + '&series=EQ')
    q.add_header('Referer',
                 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=' + stk)
    q.add_header('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
    a = urlopen(q).read()
    print(a)
    quote = json.loads(a.decode("utf-8"))
    return quote


def filter_by_vol(sdf,filter_vol):
    #df=df.loc[(df['avgVolTms'] > 0.15)]
    sdf = sdf.query('avgVolTms > '+filter_vol)
    return sdf

def to_html(sdf):
    df_html=''
    try:
        df_style=sdf.style.applymap(color_negative_red,subset=['per','changePricePer','chPer_t1','chPer_t2','chPer_t3','chPer_t4'])
        df_html = str(df_style.render())
    except:
        print("___________________________ERROR WHILE FORMATING__________________________________*******")
        traceback.print_exc()
    return df_html
def sort_price_vol_times(sortByVolTimes,lstUpdateTime,new_skts):
    sVolTimes1 = to_html(sortByVolTimes)
    change_vol_df=filter_by_vol(sortByVolTimes,'0.2')
    print("Filterd change volume *************************************")
    print(change_vol_df)
    sChangeVol=to_html(change_vol_df.sort_values(by=['changeVol'], ascending=[0]))
    if is_closing_bell():
        write_df_to_file(sortByVolTimes)
    #sChangeVolPrev4=to_html(change_vol_df.sort_values(by=['changeVol_prev'], ascending=[0]))
    #sChangePricePer = to_html(change_vol_df.sort_values(by=['changePricePer'], ascending=[0]))
    sPricePer = to_html(sortByVolTimes.sort_values(by=['per'], ascending=[0]))
    #sValue = to_html(sortByVolTimes.sort_values(by=['mVal'], ascending=[0]))
    sChangePer = to_html(sortByVolTimes.sort_values(by=['chPer_tot'], ascending=[0]))
    format_new_stocks=''
    formatedTxt="<br> NSE TIME " + lstUpdateTime +\
        "<table border='1' colspan='10'><tr><td>Average Volume times surges </td></tr></table>" + sVolTimes1 \
                +"<table border='1' colspan='10'><tr><td>Change Price  </td></tr></table>" + sChangePer \
                + "<table border='1' colspan='10'><tr><td>Change Volume   </td></tr></table>" + sChangeVol

    return formatedTxt
def write_df_to_file(df):
    now = datetime.datetime.now()
    file_name = "./data/NIFTY50_AVGVOLTIMES_%d_%d_%d" % (now.day, now.month, now.year) + ".csv"
    df.to_csv(file_name, sep='\t')
def is_closing_bell():
    now = datetime.datetime.now()
    if now.hour > 15 and now.minute > 25:
        return True
def merge_last_quotes(queue,latestQuotes):
    try:
        if len(queue) != 4:
            return "***************Error in the data frame size is not correct"
        df = queue[0]
        i=0
        for df_ in queue:
            if i>0:
                df = df.merge(df_ ,on='symbol', how='right', suffixes=('_t'+str(i), '_t'+str(i+1)))
            i=i+1
        df = df.merge(latestQuotes, on='symbol', how='right', suffixes=('_t' + str(i), '_latest' + str(i + 1)))
        df = df.fillna(0.0)
        df = df.sort_values(by=['avgVolTms'], ascending=[0])
    except Exception as e:
        traceback.print_exc()
        print(str(e))
    return df


def set_rank(sdf):
    rank = []
    i=1
    for row in sdf['symbol']:
       rank.append(i)
       i = i + 1
    sdf['Rank']=rank
    return sdf
def color_negative_red(val):
    color = 'red' if (isinstance(val,int) or isinstance(val,float)) and val <=0 else 'white'
    if (isinstance(val, int) or isinstance(val, float)) and val > 0:
        color='green'
    return 'border: 1px solid black;background-color: %s' % color
def getNIFTYData():
    global fileOpen,content,i
    if fileOpen==0:
        with open('NIFTY50_RAW_27_11_2019.csv') as f:
            content = f.readlines()
        fileOpen=1
    str=content[i].strip()
    i+=1
    return str
def filter1(sdf):
    sdf = sdf.loc[:, ['symbol','ltP','per_t1','per_t2','per_t3','per_t4','per','trdVol','trdVol_t4','trdVol_t1','avgVolTms','mVal','Rank_t1','Rank','avgVol'	], ]
    sdf['R1-R5']=sdf['Rank_t1'] -sdf['Rank']
    sdf['changeVol'] = (sdf['trdVol'] - sdf['trdVol_t1'])/sdf['trdVol_t1']
    sdf['changeVol_prev'] = (sdf['trdVol'] - sdf['trdVol_t4']) / sdf['trdVol_t4']
    sdf['changePricePer'] = sdf['per'] - sdf['per_t1']
    sdf['chPer_t4'] = sdf['per'] - sdf['per_t4']
    sdf['volChPer'] = (sdf['trdVol'] - sdf['trdVol_t4'])/sdf['avgVol']
    sdf['chPer_t3'] = sdf['per_t4'] - sdf['per_t3']
    sdf['chPer_t2'] = sdf['per_t3'] - sdf['per_t2']
    sdf['chPer_t1'] = sdf['per_t2'] - sdf['per_t1']
    sdf['chPer_tot'] = sdf['chPer_t4'] + sdf['chPer_t3'] +sdf['chPer_t2'] + sdf['chPer_t1']
    sdf = sdf.loc[:,
          ['symbol', 'ltP','per', 'trdVol',  'avgVolTms','mVal', 'changeVol','changeVol_prev','changePricePer'
              ,'chPer_t1', 'chPer_t2',
           'chPer_t3', 'chPer_t4','chPer_tot','volChPer'], ]

    sdf = sdf.replace([np.inf, -np.inf], 0)
    sdf = sdf.fillna(0.0)
    sdf = sdf.round(3)
    return sdf
def openURL():
    q = Request('https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json')
    q.add_header('X-Requested-With', 'XMLHttpRequest')
   # q.add_header('', '')
    q.add_header('Upgrade-Insecure-Requests', '1')
    #q.add_header('', '')

    q.add_header('Host', 'www.nseindia.com')

    q.add_header('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
    q.add_header('Cookie','_ga=GA1.2.679108027.1550425498; _gid=GA1.2.457999525.1575394890; instrument3=FUTSTK; optiontype3=-; expiry3=26DEC2019; strikeprice3=-; instrument4=FUTSTK; expiry4=26DEC2019; optiontype4=-; strikeprice4=-; sym1=TATAMOTORS; underlying1=BANKNIFTY; strikeprice1=32000.00; optiontype1=PE; instrument1=OPTIDX; expiry1=; optiontype2=PE; strikeprice2=12000.00; instrument2=OPTIDX; expiry2=; underlying2=NIFTY; sym2=TITAN; sym3=INDIGO; underlying3=INDIGO; sym4=GODREJCP; pointer=5; sym5=ICICIBANK; pointerfo=4; underlying4=ICICIBANK; bm_mi=0D1B724D0DD2556D48EEC253859F4948~b78qLOwSbZAx6C7mgIAwEwWAbyZROmfwzQwjponvurUW1iWXmYZJ0ir0mKtsCoaS867zLLJIfzoM7dxg3b+XlTYynfMm6R079adjV0Hal0auP3+OdtPPfzkXQrIUneQeUYeKV2GZl2G0oKhldUWmQUfzIH+vNmhoF+/ceOsID0+vnh/fStByi5n96j+jhwMqfZTtHrxL4oa5/qrK2CzRa4qdt3fEo8tEYdjx3A5tAmNyydKA99Xm81sMY2JcDNk1P2w8nbKdidcTxRSzMRZzF2b7/v4MwMkrGlxgSrvNTaRTIn0UjR4RMpGOzmMzfiDL1eWyxpwsxU9ZG/+FwXH4Fw==; ak_bmsc=3FE3CC3983BDC20B64F35407466C6E1517417C43574D000045CDE95DD2102167~plJacoRXJ/THkUfJOvVU4IY28bdyH5ljQW7E5XUtfrk3KiwpYjEDkmNUp10hcIVGBUEP+nO/CmrOqeUnKhTqTEP3YQy5YvXXRuaQsGcoiFqfBmL8FBiDMcRdNaUgAls2VdjGTT+VKiPaayf3PmC1xkSZL5eyK/eVY4s6leYYT2oVsV8Lhpe8VEVPoY1SkRlEjsUNmWYI+mogbgBfvnQyiCNO0nRQmYf0QTKJY6Q7d1pX16/14/3cX+SkunvXV2M+pt; RT="z=1&dm=nseindia.com&si=3a4c35b2-4205-4e36-ac11-ffb00fa5ff55&ss=k3tlncj7&sl=4&tt=wmi&bcn=%2F%2F684d0d3b.akstat.io%2F"; bm_sv=9698BC70B283A46DB6C939D523CC43C8~xLBQXtg332eOKjm1s/ZRppswoCEG/7XkEmb1eaw54T+kLUfeGdMYn9QJ2CcRWZVA0ZsVjZgxOJMr4RCz6KP+QKwo1VtgAdRjwZ8vrGsS5B4XgP3k1yK83heKf5AGHKitF30PInwRvLCmQBAuXk/cJkpQptDfKtlC5x2b88MUAOU=')
    return q
def write_to_file(rawFile,msg):
    rawFile.write(msg)
    rawFile.flush()
def change_wait_time():
    now = datetime.datetime.now()
    if now.hour == 9 and now.minute < 46:
        return 60
    return 120
wait_time=30
avgVolDF = DataFrame.from_dict(avgVolArr, orient='columns')#pd.DataFrame.from_items(avgVolArr)
now = datetime.datetime.now()
#fileName = "./data/NIFTY50_%d_%d_%d" % (now.day, now.month, now.year) + ".csv"
fileJSONName = "./data/NIFTY50_RAW_%d_%d_%d" % (now.day, now.month, now.year) + ".csv"
#f = open(fileName, 'a')
rawFile = open(fileJSONName, 'a')
prev_df=''
i=0
content=''
fileOpen=0
queue = deque([], maxlen=4)
pd.set_option('display.max_columns', None)
prevTime=''
q = openURL()
prev_nifty=0
def is_prev_day(data):
    lstUpdateTime = data['time']
    return "15:59:" in lstUpdateTime or "16:00:" in lstUpdateTime
while (1):
    try:
        a = urlopen(q).read()#getNIFTYData()#
        if len(a) <1 :
            continue
        data = json.loads(a)
        lstUpdateTime = data['time']
        if is_prev_day(data) :
            time.sleep(wait_time)
            continue
        if prevTime == lstUpdateTime:
             print('SAME RESPONSE OR OUT OF TRADING HOURS will WILL RETRY AFTER '+str(wait_time))
             time.sleep(wait_time)
             continue
        wait_time = change_wait_time()
        print("wait time is " + str(wait_time))
        write_to_file(rawFile, "\n" + str(a).rstrip())
        df = DataFrame.from_dict(data['data'], orient='columns')
        origi_sdf =perProcessing(df,lstUpdateTime,avgVolDF)
        sdf=filter_stocks(origi_sdf)
        pdat = getSummary(data,prev_nifty)
        formatedTxt = to_html(sdf)
        hdr = header(sdf, lstUpdateTime, pdat)
        formatedTxt = hdr + '<br/>' + formatedTxt
        nifty_curr = data['latestData'][0]['ch']
        print('leng of queue is {}'.format(len(queue)))
        if len(queue) >3:
            merged = merge_last_quotes(queue,sdf)#pd.merge(sdf, prev_df, on='symbol', how='outer')
            print(merged)
            pdat = getSummary(data,prev_nifty)
            hdr = header(sdf, lstUpdateTime, pdat)
            print("Summar is "+pdat)
            print("Header is " + hdr)
            filtered=filter1(merged)
            formatedTxt = sort_price_vol_times(filtered, lstUpdateTime, '')
            formatedTxt = hdr + '<br/>' + formatedTxt

        prev_nifty = nifty_curr
        prev_df = origi_sdf
        outlook(pdat, formatedTxt)
        queue.append(origi_sdf)
        prevTime=lstUpdateTime
    except TimeoutError as e:
        traceback.print_exc(e)
        print(str(e))
    print('Waiting .... {} secs'.format( wait_time))
    time.sleep(wait_time)
