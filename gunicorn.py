'''
Author : hupeng
Time : 2021/10/12 15:46 
Description: 
'''
from gevent import monkey;monkey.patch_all()
import multiprocessing

# debug = True
loglevel = 'info'
bind = "0.0.0.0:8977"
pidfile = "/xdfapp/logs/ocrquesseg-svr/gunicorn/gunicorn.pid"
accesslog = "/xdfapp/logs/ocrquesseg-svr/gunicorn/access.log"
errorlog = "/xdfapp/logs/ocrquesseg-svr/gunicorn/error.log"
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
daemon = False
# chdir = '/xdfapp/apps/ocrquesseg-svr'
chdir = '/home/hupeng/project/ocrquesseg-svr'
worker_connections = 500
timeout = 300
#max_requests = 1000
#max_requests_jitter = 1000
keepalive = 5
worker_class = 'gevent' # gevent 1.1 eventlet sync 2.3 gthread 2.2

# 启动的进程数
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
threads = 1
