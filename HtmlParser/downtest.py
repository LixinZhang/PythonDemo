'''
Created on 2012-3-12

@author: xiaojay
'''
import urllib2
def downPage(url):
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req)
    return fd.read()

text = downPage("http://www.cnblogs.com/coser")
print text