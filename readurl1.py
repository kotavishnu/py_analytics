import urllib.request
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
fw = open('workfile', 'w')
with opener.open('http://www.justdial.com/Hyderabad/chit-fund-companies/') as f:
	dat=f.read()
	print(dat)
	fw.write(str(dat))
fw.close()