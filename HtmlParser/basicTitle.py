#-*- encoding: gb2312 -*-
'''
Created on 2012-1-9
@author: xiaojay
'''

from HTMLParser import HTMLParser
import urllib2
from htmlentitydefs import entitydefs

"""
HTMLParser��python��������html��ģ�顣�����Է�����html����ı�ǩ�����ݵȵȣ���һ�ִ���html�ļ��;���� 
HTMLParser���õ���һ���¼�������ģʽ����HTMLParser�ҵ�һ���ض��ı��ʱ������ȥ����һ���û�����ĺ������Դ���֪ͨ������
����Ҫ���û��ص�����������������handler_��ͷ�ģ�����HTMLParser�ĳ�Ա������
������ʹ��ʱ���ʹ�HTMLParser�������µ��࣬Ȼ �����¶����⼸����handler_��ͷ�ĺ������ɡ�
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
    #����ʵ������            
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