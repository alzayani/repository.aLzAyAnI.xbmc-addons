import  urllib,urllib2,time,re


url="http://moshahda.net/sjzzht84xhsx"
req = urllib2.Request(url)
time.sleep(10)
response = urllib2.urlopen(req)
html = response.read()
response.close()
id = re.findall('<input type="hidden" name="id" value="(.*?)">',html, re.M|re.I)[0]
fname = re.findall('<input type="hidden" name="fname" value="(.*?)">',html, re.M|re.I)[0]
hash = re.findall('<input type="hidden" name="hash" value="(.*?)">',html, re.M|re.I)[0]
action = re.findall('''<Form method="POST" action='(.*?)'>''',html, re.M|re.I)[0]
print "id,fname,hash,action",id,fname,hash,action
data= {
    'imhuman': "Proceed to video",    
    'op': 'download1',
    'usr_login': '',
    'id': id,
    'fname': fname,
    'referer': '',
    'method': 'POST',
    'action': action,
    'hash': hash}   

info = urllib.urlencode(data)   

			
req = urllib2.Request(url, info)
#time.sleep(10)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

response = urllib2.urlopen(req)
link=response.read()
response.close()
print link
