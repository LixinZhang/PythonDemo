'''
Created on 2012-1-9
Use Get Method to get weather info from web
@author: xiaojay
'''
#-*- encoding: gb2312 -*-

import sys
import urllib2 , urllib
import HTMLParser



zipcode = "nanjing"
url = "http://www.wunderground.com/cgi-bin/findweather/getForecast"
data = urllib.urlencode([('query',zipcode)])
req = urllib2.Request(url)
fd = urllib2.urlopen(url, data)

while True:
    data = fd.read(1024)
    if data :
        print data
    else:
        break
