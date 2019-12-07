import datetime
import sys
import time
import json
import smtplib

from urllib2 import Request, urlopen  # Python 2
q = Request('https://www.nseindia.com/live_market/dynaContent/live_analysis/volume_spurts/volume_spurts.json')
q.add_header('X-Requested-With', 'XMLHttpRequest')
q.add_header('Cookie', 'pointer=1; sym1=INFY')
q.add_header('Host', 'www.nseindia.com')
q.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
q.add_header('Content-Type', 'text/html;charset=ISO-8859-1')
q.add_header('Referer', 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY')
q.add_header('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')

def send_email(user, pwd, recipient, subject, body) :
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print( 'successfully sent the mail')
    except:
        print ("failed to send mail")

try:
    send_email('xxxxx', 'xxxx', 'xxxxxx', 'Volume STOCKS Started', '')
    while (1):
        now = datetime.datetime.now()
        min=now.minute
        hour = now.hour + 5
        if(min>30):
            min=(min+30)%60
            hour=hour+1
        if(hour>23):
            hour=hour%24
        print("current hour "+str(hour)+" mins"+str(min))
        if (hour >= 16):
            sys.exit()
        if hour < 9 or (hour == 9 and min < 15):
            print("Waiting.....")
            time.sleep(300)
            continue
        a = urlopen(q).read()
        #print(a)
        data = json.loads(a.decode("utf-8"))
       # print ("data "+str(data))
        msg = '\nSYMBOL\tPRIC\tCHANGE\tVOLUME\tAVG\tPERCENT CHANGE VOLUME\n'
        stocks = ""
        for majorkey in data['data']:
            chn=float(majorkey['netpr'])
            majorkey['turn_lkh']=str(majorkey['turn_lkh']).replace(',', '')
            #print("turn over "+majorkey['turn_lkh'])
            vol=float(majorkey['turn_lkh'])
            majorkey['week2a'] = str(majorkey['week2a']).replace(',', '')
            wavol = float(majorkey['week2a'])
            majorkey['ltp'] = str(majorkey['ltp']).replace(',', '')
            pri= float(majorkey['ltp'])
            if(chn>1 and vol>100000 and vol>wavol*(1/5) and pri >100):
                print(majorkey['sym']+","+majorkey['ltp']+","+majorkey['netpr']+","+majorkey['turn_lkh']+","+majorkey['week2a']+","+str((vol/wavol)))
               # msg=msg+'<TR><TD>'+majorkey['sym']+'</TD><TD>'+majorkey['ltp']+'</TD><TD>'+majorkey['netpr']+'</TD><TD>'+majorkey['turn_lkh']+'</TD><TD>'+majorkey['week2a']+'</TD><TD>'+str((vol/wavol))+'</TD></TR>'
                stocks = stocks+ '\n' + majorkey['sym'] + '\t' + majorkey['ltp'] + '\t' + majorkey['netpr'] + '\t' + majorkey['turn_lkh'] + '\t' + majorkey['week2a'] + '\t' + str((vol / wavol)*100) + '\n'
        if(len(stocks)>0):
            send_email('xxxxm', 'xxxx$xxx', 'xx.xx@xx.com', 'Volume STOCKS', msg+stocks)
        print("Waiting.....")
        time.sleep(600)
        #send_mail('xx@xx.com', 'xxx$x', msg)
finally:
    print ("Before exit")

