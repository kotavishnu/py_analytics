try:
    from urllib.request import Request, urlopen  # Python 3
except:
    from urllib2 import Request, urlopen  # Python 2
	
req = Request('http://www.justdial.com/functions/ajxsearch.php?national_search=0&act=pagination&city=Hyderabad&search=Chit+Fund+Companies&where=&catid=462479&psearch=&prid=&page=1&SID=&mntypgrp=0&toknbkt=&bookDate=&jdsrc=')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
resp = urlopen(req)
content = resp.read()
print(content)