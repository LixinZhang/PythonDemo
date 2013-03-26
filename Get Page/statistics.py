'''
Created on 2012-3-12

@author: xiaojay
'''

timeout = 5
fetched_url = 0
failed_url = 0
timeout_url = 0
trytoomany_url =0
other_url = 0
max_try_times = 3
total_url = 0


DNSCache = {}

RESULTOTHER = 0 #Other faults
RESULTFETCHED = 1 #success
RESULTCANNOTFIND = 2 #can not find 404
RESULTTIMEOUT = 3 #timeout
RESULTTRYTOOMANY = 4 #too many tries