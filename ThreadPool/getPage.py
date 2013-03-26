'''
Created on 2012-3-12
test
@author: xiaojay
'''

import threadpool 
import urllib2
import datetime
import statistics

import socket
socket.setdefaulttimeout(5)

def downPage(url):
    try:
        req = urllib2.Request(url)
        fd = urllib2.urlopen(req)
        return url ,fd.read()
    except Exception ,e:
        statistics.total_url_fetched+=1
        print statistics.total_url_fetched,"\tfailed :",url,
        print e
        print '-----------'
        #print url,

def writeFile(request,result):
    f = open("downloadPage2/"+str(request.requestID),'w')
    f.write(result[1])
    f.flush()
    f.close()
    statistics.total_url_fetched+=1
    print statistics.total_url_fetched,'\tfetched :', result[0],

def work():
    limit = 500
    urlset = open("input2.txt","r")
    start = datetime.datetime.now()
    print "Start at :\t" , start    
    main = threadpool.ThreadPool(60)
    
    
    for url in urlset :
        try :
            req = threadpool.WorkRequest(downPage,args=['http://'+url],kwds={},callback=writeFile)
            main.putRequest(req)
        except Exception:
            print Exception.message
        
    while True:
        try:
            main.poll()
            if statistics.total_url_fetched -statistics.failed_url  > limit : break
        except threadpool.NoResultsPending:
            print "no pending results"
            break
        except Exception:
            statistics.failed_url+=1

    main.stop()
    end = datetime.datetime.now()
    print "End at :\t" , end
    print "Total Cost :\t" , end - start
    print "Total urls : %d , failed urls : %d " % (statistics.total_url_fetched,statistics.failed_url)


if __name__ =='__main__':
    work()
    #print downPage("http://codex.wordpress.org:80/wordpress_semantics")
    '''
    urlset = open("input2.txt","r")
    for u in urlset:
        downPage(u)
    print 'Failed :\t' ,statistics.total_url_fetched
    '''