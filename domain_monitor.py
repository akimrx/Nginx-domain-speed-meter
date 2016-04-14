#!/usr/bin/env python
import os
import sys
import time
import pickle
import logging

import settings

cacheFile = settings.CACHE_FILE

logFile = settings.NGINX_LOG_FILE

cacheTtl = settings.CACHE_TTL

logging.basicConfig(filename=settings.LOG_FILE,level=settings.LOG_LEVEL)

type, domain = sys.argv[1:]


def cacheFileMtime(cache_file):
    try:
        mtime = os.path.getmtime(cache_file)
    except OSError:
        return cacheTtl + 1
    return (time.time()-mtime)/60


def cacheUpdate(cache_file, log_file):
    log = open(log_file,'r')
    data = {}
    cache = {}
    line = log.readline()
    start = line.split(' ')[3]
    while line:
        domain, send, receive, timestamp = line.split(' ')
        if domain not in data:
            data[domain] = {'send':0, 'receive':0}
        else:
            data[domain]['send'] += int(send)
            data[domain]['receive'] += int(receive)
        stop = timestamp
        line = log.readline()
    timestamp = float(stop) - float(start)
    log.close()
    open(log_file, 'w').close()
    for domain in data.keys():
        sendSpeed = int(data[domain]['send']/timestamp)
        receiveSpeed = int(data[domain]['receive']/timestamp)
        cache[domain] = {}
        cache[domain]['send'] = sendSpeed
        cache[domain]['receive'] = receiveSpeed
    cache_file = open(cache_file,'wb')
    pickle.dump(cache, cache_file)
    cache_file.close()
    return cache


def getSend(domain, cache):
    return cache[domain].get('send', 0)


def getReceive(domain, cache):
    return cache[domain].get('receive', 0)


def cacheLoad(cache_file):
    cache_file=open(cache_file, 'rb')
    cache = pickle.load(cache_file)
    cache_file.close()
    return cache


def getDomains(cache):
    print "{\n"
    print "\"data\":[\n\n"
    text = []
    for key in cache.keys():
        text.append("{{\"{{#DOMAIN}}\":\"{domain}\"}}".format(domain=key))
    print ','.join(text)
    print "\n]"
    print "}\n"

if cacheFileMtime(cacheFile) < cacheTtl:
    cache=cacheLoad(cacheFile)
else:
    cache=cacheUpdate(cacheFile, logFile)

if type == 'send':
    print getSend(domain, cache),
elif type == 'receive':
    print getReceive(domain, cache),
elif type == 'list':
    getDomains(cache),
else:
    sys.exit(1)
