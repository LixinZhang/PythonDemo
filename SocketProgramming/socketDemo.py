'''
Created on 2011-12-18
Socket Demo 
@author: xiaojay
''' 

import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#port = socket.getservbyname('ftp','tcp')
port = 2015

"""
Shut down one or both halves of the connection. If how is SHUT_RD, further receives are disallowed. 
If how is SHUT_WR, further sends are disallowed. If how is SHUT_RDWR, further sends and receives are disallowed. 
Depending on the platform, shutting down one half of the connection can also close the opposite half .
"""
"""
print socket.SHUT_RD
print socket.SHUT_RDWR
print socket.SHUT_WR
"""

print "This is the client :"

try:
    s.connect(("localhost",port))
    s.sendall("1This is the message,2This is the message,3This is the message")
    s.shutdown(socket.SHUT_RD)
    #s.sendall("10100101010101010")
    while True:
        msg = s.recv(1024)
        if msg :
            print msg
        else :
            break
finally:
    s.close() 
    print "Socket is closed."




