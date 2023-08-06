import requests

import requests

from bs4 import BeautifulSoup
from datetime import * 
def infoget(user):
	headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
	data=None
	rd = requests.get(f"https://www.tiktok.com/@{user}", headers=headers).text
	try:
	 soup = BeautifulSoup(rd, 'html.parser')
	 script = soup.find(id='SIGI_STATE').contents
	 rr = str(script).split('},"UserModule":{"users":{')[1]
	 try:
	 	na=rr.split(',"nickname":"')[1].split('",')[0]
	 except:
	 	na='false'
	 try:
	 	id=rr.split('"id":"')[1].split('",')[0]
	 except:
	 	id='false'
	 try:
	 	pr=rr.split('"privateAccount":')[1].split(',')[0]
	 except:
	 	pr='false'
	 try:
	 	flog=rr.split('"followingCount":')[1].split(',')[0]
	 except:
	 	flog='0'
	 try:
	 	flos=rr.split('"followerCount":')[1].split(',')[0]
	 except:
	 	flos='0'
	 try:
	 	bio=rr.split('"signature":')[1].split(',')[0]
	 except:
	 	bio='false'
	 try:
	 	video=rr.split('"videoCount":')[1].split(',')[0]
	 except:
	 	video='false'
	 try:
	 	like= rr.split('"heartCount":')[1].split(',')[0]
	 except:
	 	like='0'
	 try:
	 	user= rr.split('"uniqueId":')[1].split(',')[0]
	 except:
	 	user='false'
	 try:
             url_id = int(id)
             binary = "{0:b}".format(url_id)
             i = 0
             bits = ""
             while i < 31:
                 bits += binary[i]
                 i += 1
             timestamp = int(bits, 2)
             timme = datetime.fromtimestamp(timestamp)
             #print(timme)
	 except:
	 	timme= 'false'
	 return {"user":user,"name":na,"id":id,"date":timme,"followers":flos,"following":flog,"privacy":pr,"like":like,"video":video,"bio":bio}
	except:
	 	return 'BAD'
