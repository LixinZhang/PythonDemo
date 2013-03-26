#-*- encoding: gb2312 -*-
'''
Created on 2012-1-9
@author: xiaojay
'''

from HTMLParser import HTMLParser
import urllib2
from htmlentitydefs import entitydefs

"""
HTMLParser是python用来解析html的模块。它可以分析出html里面的标签、数据等等，是一种处理html的简便途径。 
HTMLParser采用的是一种事件驱动的模式，当HTMLParser找到一个特定的标记时，它会去调用一个用户定义的函数，以此来通知程序处理。
它主要的用户回调函数的命名都是以handler_开头的，都是HTMLParser的成员函数。
当我们使用时，就从HTMLParser派生出新的类，然 后重新定义这几个以handler_开头的函数即可。
"""

class TitleParser (HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = ""
        self.readingtitle = False
    def handle_starttag(self,tag,attrs):
        if tag == 'title':
            self.readingtitle = True
        if attrs :
            print type(attrs)    
            print attrs
    #处理实体引用            
    def handle_entityref(self , name):
        if entitydefs.has_key(name):
            self.handle_data(name)
        else :
            self.handle_data("&"+name )
    def handle_data(self,data):
        if self.readingtitle :
            self.title+=data
    def handle_endtag(self,tag):
        if tag == 'title':
            self.readingtitle = False
    def gettitle(self):
        return self.title

url = "http://jwc.seu.edu.cn"
req = urllib2.Request(url)
fd = urllib2.urlopen(req)
#text = "<html><head><title>Test</title></head><body><title>title2222 &ram pp</title><h1>Parse me!</h1></body></html>"
text = fd.read()
#print text

#text =  fd.read()
#text = text.encode("utf8")

tp = TitleParser()
tp.feed(text)


print "Title is " , tp.gettitle()