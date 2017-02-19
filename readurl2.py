import urllib.parse
import urllib.request

url = 'http://www.justdial.com/Hyderabad/chit-fund-companies/ct-462479'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}
req = urllib.request.Request(url, '', headers)
with urllib.request.urlopen(req) as response:
   the_page = response.read()
   print(the_page)