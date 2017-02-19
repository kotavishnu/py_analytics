import json
import urllib.request
from urllib.error import HTTPError


try:

    url_address ='https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol=YESBANK&series=EQ'
    with urllib.request.urlopen(url_address) as url:
        data = json.loads(url.read())
        print(data)

except HTTPError as ex:
    print(ex.read())