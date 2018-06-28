import requests
from multiprocessing.dummy import Pool as ThreadPool
import re
from sys import argv

dotx = '.'
iprange = argv[1]

ipArr = iprange.split('.')
ipArr.pop(3)
ip = dotx.join(ipArr)

iplist = []

def coz(i):
	baglanti = requests.get("http://www.bing.com/search?q=ip%3A"+ip+"."+str(i)+"&go=Submit")
	kaynak = baglanti.text
	bingcode = kaynak.find("bulunamad")
	if bingcode == -1:
		pat = re.compile("<h2><a href=\"(.*?)\" h=\"ID=SERP",re.DOTALL|re.M)
		linkler = pat.findall(kaynak)
		for link in linkler:
			print ip+"."+str(i)+ "   "+link

for i in range(0,255):
	iplist.append(i)

pool = ThreadPool(20)

results = pool.map(coz, iplist)

pool.close()
pool.join()
