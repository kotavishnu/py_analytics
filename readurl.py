import urllib.request
req = urllib.request.Request('http://www.justdial.com/Hyderabad/chit-fund-companies/ct-462479')
f = open('workfile', 'wb')
with urllib.request.urlopen(req) as response:
   the_page = response.read()
   print(the_page)
   f.write(the_page)
f.close();   
   
