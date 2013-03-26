'''
Created on 2012-3-13
Get Page using GET method
Default using HTTP Protocol , http port 80
@author: xiaojay
'''
import socket
import statistics
import datetime
import threading

socket.setdefaulttimeout(statistics.timeout)

class Error404(Exception):
    '''Can not find the page.'''
    pass

class ErrorOther(Exception):
    '''Some other exception'''
    def __init__(self,code):
        #print 'Code :',code
        pass
class ErrorTryTooManyTimes(Exception):
    '''try too many times'''
    pass

def downPage(hostname ,filename , trytimes=0):
    try :
        #To avoid too many tries .Try times can not be more than max_try_times
        if trytimes >= statistics.max_try_times : 
            raise ErrorTryTooManyTimes
    except ErrorTryTooManyTimes :
        return statistics.RESULTTRYTOOMANY,hostname+filename
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        #DNS cache
        if statistics.DNSCache.has_key(hostname):
            addr = statistics.DNSCache[hostname]
        else:
            addr = socket.gethostbyname(hostname)
            statistics.DNSCache[hostname] = addr
        #connect to http server ,default port 80
        s.connect((addr,80))
        msg  = 'GET '+filename+' HTTP/1.0\r\n'
        msg += 'Host: '+hostname+'\r\n'
        msg += 'User-Agent:xiaojay\r\n\r\n'
        code = '' 
        f = None
        s.sendall(msg)
        first = True
        while True:
            msg = s.recv(40960)
            if not len(msg):
                if f!=None:
                    f.flush()
                    f.close()
                break
            # Head information must be in the first recv buffer
            if first:
                first = False                
                headpos = msg.index("\r\n\r\n")
                code,other = dealwithHead(msg[:headpos])
                if code=='200':
                    #statistics.fetched_url += 1
                    f = open('pages/'+str(abs(hash(hostname+filename))),'w')
                    f.writelines(msg[headpos+4:])
                elif code=='301' or code=='302':
                    #if code is 301 or 302 , try down again using redirect location
                    print 'ksjdhfksjfjd',hostname,filename;
                    if other.startswith("http") :                
                        hname, fname = parse(other)
                        downPage(hname,fname,trytimes+1)#try again
                    else :
                        downPage(hostname,other,trytimes+1)
                elif code=='404':
                    raise Error404
                else : 
                    raise ErrorOther(code)
            else:
                if f!=None :f.writelines(msg)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return statistics.RESULTFETCHED,hostname+filename
    except Error404 :
        return statistics.RESULTCANNOTFIND,hostname+filename
    except ErrorOther:
        return statistics.RESULTOTHER,hostname+filename
    except socket.timeout:
        return statistics.RESULTTIMEOUT,hostname+filename
    except Exception, e:
        return statistics.RESULTOTHER,hostname+filename

    

def dealwithHead(head):
    print head
    '''deal with HTTP HEAD'''
    lines = head.splitlines()
    fstline = lines[0]
    code =fstline.split()[1]
    if code == '404' : return (code,None)
    if code == '200' : return (code,None)
    if code == '301' or code == '302' : 
        for line in lines[1:]:
            p = line.index(':')
            key = line[:p]
            if key=='Location' :
                return (code,line[p+2:])
    return (code,None)
    
def parse(url):
    '''Parse a url to hostname+filename'''
    try:
        u = url.strip().strip('\n').strip('\r').strip('\t')
        if u.startswith('http://') :
            u = u[7:]
        elif u.startswith('https://'):
            u = u[8:]
        if u.find(':80')>0 :
            p = u.index(':80')
            p2 = p + 3
        else:
            if u.find('/')>0:
                p = u.index('/') 
                p2 = p
            else:
                p = len(u)
                p2 = -1
        hostname = u[:p]
        if p2>0 :
            filename = u[p2:]
        else : filename = '/'
        return hostname, filename
    except Exception ,e:
        print "Parse wrong : " , url
        print e

def downPageEcho(hostname ,filename):
    '''not save to files'''
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr = socket.gethostbyname(hostname)
        s.connect((addr,80))
        msg  = 'GET '+filename+' HTTP/1.0\r\n'
        msg += 'Host: '+hostname+'\r\n'
        msg += 'User-Agent:xiaojay2\r\n\r\n'
        s.sendall(msg)
        first = True
        while True:
            msg = s.recv(20480)
            if not len(msg):
                break
            if(first):
                headpos = msg.index("\r\n\r\n")
                print dealwithHead(msg[:headpos])
                first = False
    except socket.timeout:
        print "timeout ", hostname+filename
    except Exception, e:
        print e ,"Some Wrong at", hostname,filename

def PrintDNSCache():
    '''print DNS dict'''
    n = 1
    for hostname in statistics.DNSCache.keys():
        print n,'\t',hostname, '\t',statistics.DNSCache[hostname]
        n+=1

def dealwithResult(res,url):
    '''Deal with the result of downPage'''
    statistics.total_url+=1
    if res==statistics.RESULTFETCHED :
        statistics.fetched_url+=1
        print statistics.total_url , '\t fetched :', url
    if res==statistics.RESULTCANNOTFIND :
        statistics.failed_url+=1
        print "Error 404 at : ", url
    if res==statistics.RESULTOTHER :
        statistics.other_url +=1
        print "Error Undefined at : ", url
    if res==statistics.RESULTTIMEOUT :
        statistics.timeout_url +=1
        print "Timeout ",url
    if res==statistics.RESULTTRYTOOMANY:
        statistics.trytoomany_url+=1
        print e ,"Try too many times at", url

if __name__=='__main__':    
    print  'Get Page using GET method'
    
