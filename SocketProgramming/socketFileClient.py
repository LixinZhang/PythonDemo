'''
Created on 2011-12-18
Socket using makefile
@author: xiaojay
'''

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("localhost",2015))

message = "This is the message to be sent !"

try:
    f = s.makefile("rw",0)
    f.write(message)
    f.flush()
    print "read..."
    
    for item in f.readlines():
        print item
finally:
    #s.close()
    print "Socket is closed !"