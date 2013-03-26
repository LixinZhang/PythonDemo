"""
Created on 2012-1-7
@author: xiaojay
"""
import urllib2

"""
The urllib2 module defines functions and classes which help in opening URLs 
(mostly HTTP) in a complex world - basic and digest authentication, redirections, cookies and more.
"""

#url = "http://cse.seu.edu.cn/jx/MailPage.aspx"
url = "http://www.baidu.com"

#Create a Request object
req = urllib2.Request(url)

#Returns a file-like object with two additional methods
fd = urllib2.urlopen(req)

print "The url is : " , fd.geturl() 
info = fd.info()
 
print len(info)
print info

"""
while True :
    data = fd.read(1024)
    if not data:
        break
    print data
"""    