#!/usr/bin/python
# -*- coding: utf-8 -*-

# İllegalsecurity
# Coded by CodeNinja
# http://www.codeninja.cf
# http://www.illegalsecurity.com

import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize

hedef = raw_input("Hedef / Target : ")

print "TARANIYOR / SCANNING ..."

url = hedef
tarayici = mechanize.Browser()
urls = [url]
gez = [url]

while len(urls)>0:
    try:
        tarayici.open(urls[0])
        urls.pop(0)
        for link in tarayici.links():
            yeniurl =  urlparse.urljoin(link.base_url,link.url)
            if yeniurl not in gez and url in yeniurl:
                gez.append(yeniurl)
                urls.append(yeniurl)
                print yeniurl
    except:
        # print "aynı olan linkler silindi"
        urls.pop(0)

print "Bitti / Finish"


