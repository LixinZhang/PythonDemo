#-*-encoding:utf-8-*-
'''
Created on 2012-3-12
Test 
@author: xiaojay
'''
import socket
import urllib2
import datetime
import time
import statistics

socket.setdefaulttimeout(5)

def downPage(url):
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req)
    return fd.read()

def work():
    urlset = open("input.txt","r")
    start = datetime.datetime.now()
    print "Start at :\t" , start
    limit = 300
    statistics.total_url_fetched = 1;
    failed = 0;
    for url in urlset :
        try :
            text = downPage(url)
            filename = 'downloadPageUsingUrllib2/' + str(statistics.total_url_fetched)
            f = open(filename,'w')
            f.write(text)
            f.flush()
            f.close()
            print statistics.total_url_fetched , '\t fetched :', url
        except Exception:
            failed+=1
            print Exception.message
        statistics.total_url_fetched+=1
        if statistics.total_url_fetched>limit: break
    
    end = datetime.datetime.now()
    print "End at :\t" , end
    print "Total Cost :\t" , end - start
    print "Total urls : %d , failed urls : %d " %( statistics.total_url_fetched, failed)
    
work()