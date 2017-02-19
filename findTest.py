import re

html_text = open('workfile', 'r').read()
html_text=html_text.replace('\\r\\n','').replace('\\t','').replace('\\','')
#html_text=html_text.replace('\\t','');
#html_text=html_text.replace('\\','');
#print ("data is ****************************")
#print(html_text)
#text_filtered = re.sub(r'<li (.*?)>.*</li>', '', html_text)
output  = re.compile('<a onclick=.*?>.*?<span class="desk-add', re.DOTALL |  re.IGNORECASE).findall(html_text)
retag  = re.compile('<a onclick=.*?>.*?</a>', re.DOTALL |  re.IGNORECASE)
rephone  = re.compile('<b>.*?</b>', re.DOTALL |  re.IGNORECASE)
print("tags are ******************")
#print( output)
cleanr = re.compile('<.*?>')
for s in output:
	#print(s)
	chits=retag.findall(s)
	chits = re.sub('<[^>]*>', '', chits[0])
	phone=rephone.findall(s)
	phone = re.sub('<[^>]*>', '', phone[0])
	print(chits)
	print(phone)
	print("\n")