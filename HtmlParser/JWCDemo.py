#-*- encoding:gb2312 -*-
'''
Created on 2012-1-9

@author: xiaojay
'''

from HTMLParser import HTMLParser
from htmlentitydefs import entitydefs

import urllib2

url = "http://jwc.seu.edu.cn"

class NewsParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.link = ""
        self.text = ""
        self.items = [] #保存提取结果
        self.flag = False
        self.parse_date = False
        self.date_start = False
    def handle_starttag(self,tag,attrs):
        #处理开始标签
        if tag=='a' and attrs:
            for key ,value in attrs:
                if key=='href':
                    index = value.find("?")
                    if index>0 and value[0:index]=="/admin/disp.asp":
                        self.flag = True
                        self.parse_date = True             
                        self.link = value
        if tag == "td" and self.parse_date == True :
            self.date_start = True
                        
    def handle_data(self,data):
        #处理数据
        if self.flag == True :
            self.text = data
        if self.date_start == True :
            self.items.append((self.text,self.link,data))
    def handle_entityref(self , name):
        #处理实体引用
        if entitydefs.has_key(name):
            self.handle_data(name)
        else :
            self.handle_data("&"+name )
    def handle_endtag(self,tag):
        #处理结束标签
        if tag == 'a' and self.flag== True :
            self.flag = False
        if tag == 'td' and self.parse_date and self.date_start :
            self.parse_date = False
            self.date_start = False
    def getItems(self):
        return self.items
    

req = urllib2.Request(url)
fd = urllib2.urlopen(req)

newsparser = NewsParser()
#调用feed方法，开始处理
newsparser.feed(fd.read())
items = newsparser.getItems()
for text , link , date in items :
    print text , link , date
                        
                            