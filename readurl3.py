import urllib.parse
import urllib.request

url = 'http://www.justdial.com/functions/ajxsearch.php?national_search=0&act=pagination&city=Hyderabad&search=Chit+Fund+Companies&where=&catid=462479&psearch=&prid=&page=2&SID=&mntypgrp=0&toknbkt=&bookDate=&jdsrc='
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
req = urllib.request.Request(url, '', headers)
with urllib.request.urlopen(req) as response:
   the_page = response.read()
   print(the_page)