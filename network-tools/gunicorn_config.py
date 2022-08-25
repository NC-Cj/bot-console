# 日志配置
# loglevel = "debug"
# accesslog = './log/access.log'
# errorlog = './log/error.log'

debug = False
daemon = False
# preload_app = True

timeout = 120
workers = 4

worker_class = "gevent"
bind = "0.0.0.0:8080"
