'''
Created on 2012-1-7

@author: xiaojay
'''

import urllib2

class TerminalPassword(urllib2.HTTPPasswordMgr):
    def find_user_password(self, realm, authuri):
        print "2222"
        retval = urllib2.HTTPPasswordMgr.find_user_password(self, realm, authuri)
        if retval[0] == None and retval[1] == None:
            #Did not find it in store values ; prompt user
            print "Login required for %s at %s\n" % (realm,authuri)
            username = raw_input("Username : ").rstrip()
            password = raw_input("Password : ").rstrip()
            return (username,password)
        else :
            print "12123123"
            return retval


#url = "http://www.baidu.com"
url = "http://www.unicode.org/mail-arch/unicode-ml/"
req = urllib2.Request(url)
opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(TerminalPassword()))
fd = opener.open(req)

print "The url is : " , fd.geturl() 
info = fd.info()
print info