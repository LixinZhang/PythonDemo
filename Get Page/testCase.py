'''
Created on 2012-3-16

@author: xiaojay
'''
import fetchPage
import threadpool
import datetime
import statistics
import urllib2


'''one thread'''
def usingOneThread(limit):
    urlset = open("input.txt","r")
    start = datetime.datetime.now()
    for u in urlset:
        if limit <= 0 : break
        limit-=1
        hostname , filename = fetchPage.parse(u)
        res= fetchPage.downPage(hostname,filename,0)
        fetchPage.dealwithResult(res)
    end = datetime.datetime.now()
    print "Start at :\t" , start
    print "End at :\t" , end
    print "Total Cost :\t" , end - start
    print 'Total fetched :', statistics.fetched_url
    

'''threadpoll and GET method'''
def callbackfunc(request,result):
    fetchPage.dealwithResult(result[0],result[1])

def usingThreadpool(limit,num_thread):
    urlset = open("input.txt","r")
    start = datetime.datetime.now()
    main = threadpool.ThreadPool(num_thread)
    for url in urlset :
        try :
            hostname , filename = fetchPage.parse(url)
            req = threadpool.WorkRequest(fetchPage.downPage,args=[hostname,filename],kwds={},callback=callbackfunc)
            main.putRequest(req)
        except Exception:
            print Exception.message        
    while True:
        try:
            main.poll()
            if statistics.total_url >= limit : break
        except threadpool.NoResultsPending:
            print "no pending results"
            break
        except Exception ,e:
            print e
    end = datetime.datetime.now()
    print "Start at :\t" , start    
    print "End at :\t" , end
    print "Total Cost :\t" , end - start
    print 'Total url :',statistics.total_url
    print 'Total fetched :', statistics.fetched_url
    print 'Lost url :', statistics.total_url - statistics.fetched_url
    print 'Error 404 :' ,statistics.failed_url
    print 'Error timeout :',statistics.timeout_url
    print 'Error Try too many times ' ,statistics.trytoomany_url
    print 'Error Other faults ',statistics.other_url
    main.stop()

'''threadpool and urllib2 '''
def downPageUsingUrlib2(url):
    try:
        req = urllib2.Request(url)
        fd = urllib2.urlopen(req)
        f = open("pages/"+str(abs(hash(url))),'w')
        f.write(fd.read())
        f.flush()
        f.close()
        return url ,'success'
    except Exception:
        return url , None
    
def writeFile(request,result):
    statistics.total_url += 1
    if result[1]!=None :
        statistics.fetched_url += 1
        print statistics.total_url,'\tfetched :', result[0],
    else:
        statistics.failed_url += 1
        print statistics.total_url,'\tLost :',result[0],

def usingThreadpoolUrllib2(limit,num_thread):
    urlset = open("input.txt","r")
    start = datetime.datetime.now()   
    main = threadpool.ThreadPool(num_thread)    
    
    for url in urlset :
        try :
            req = threadpool.WorkRequest(downPageUsingUrlib2,args=[url],kwds={},callback=writeFile)
            main.putRequest(req)
        except Exception ,e:
            print e
        
    while True:
        try:
            main.poll()
            if statistics.total_url  >= limit : break
        except threadpool.NoResultsPending:
            print "no pending results"
            break
        except Exception ,e:
            print e 
    end = datetime.datetime.now()    
    print "Start at :\t" , start 
    print "End at :\t" , end
    print "Total Cost :\t" , end - start
    print 'Total url :',statistics.total_url
    print 'Total fetched :', statistics.fetched_url
    print 'Lost url :', statistics.total_url - statistics.fetched_url
    main.stop()

if __name__ =='__main__':
    '''too slow'''
    #usingOneThread(100)
    '''use Get method'''
    usingThreadpool(3000,50)
    '''use urllib2'''
    #usingThreadpoolUrllib2(3000,50)