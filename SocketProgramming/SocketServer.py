'''
Created on 2011-12-15
Socket Server by Python
@author: Peter
'''
import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('localhost',2015)
sock.bind(server_address)
sock.listen(10)
"""
#Nonblocking Communication and Timeouts
sock.setblocking(0)
sock.settimeout(5)
"""
print "This is the server :"
print 'bind and listen has completed !'


while True:
    print 'accept start'
    connection,client_address = sock.accept()
    print 'Have received a connection : ', client_address
    try:
        while True:
            #buffer size means the maximum amount of data to be received at once
            buffersize = 16
            data = connection.recv(buffersize)
            print data
            if data:
                #print 'sending data back to client'
                print 'length : ' , len(data) , data
                connection.sendall(data)
            else:
                #print 'no data from ', client_address
                break
            #if flag == True : break
    finally:
        connection.close()
        print "Close connection ", client_address
