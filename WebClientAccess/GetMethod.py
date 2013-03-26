'''
Created on 2012-1-7

@author: xiaojay
'''
import urllib2
import urllib

#url = "http://www.baidu.com/s?"

#url = url +  urllib.urlencode([("w","mayday")])

url = "http://www.google.com.hk/s?w=hello"
 
req = urllib2.Request(url)
fd = urllib2.urlopen(req)

while True:
    data = str(fd.read(120))
    data = data.encode("gbk")
    if data:
        print data
    else :
        break