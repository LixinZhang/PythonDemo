'''
Created on 2012-3-13

@author: xiaojay
'''

import Queue
import time
import datetime

q = Queue.Queue()

while True:
    try :
        print datetime.datetime.now()
        q.put("aaa", True, 2)
        print datetime.datetime.now()
        print q.qsize() ,
        item = q.get(timeout=4)
        print item
    except Queue.Empty:
        print Queue.Empty
