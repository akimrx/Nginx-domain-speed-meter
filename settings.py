"""
Cache ttl in minutes
Log levels
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
"""

NGINX_LOG_FILE = '/var/log/nginx/access_test.log'
CACHE_FILE = '/tmp/domain.cache'
CACHE_TTL = 5
LOG_LEVEL = 0
LOG_FILE = '/tmp/domain_monitor.log'