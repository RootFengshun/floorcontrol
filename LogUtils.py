# -*- coding: UTF-8 -*-
'''
Copyright: Copyright (c) 2018
Created on 2018-6-17
Author: fengshun
Title:  a user-defined log utils
LogUtils is a user-defined log utils of the project. It offers a a wrapper log utils on 'logging'
Provide
1.  Create log file in a thread-safe mode
2.  Called by Logger().do().log()/debug()/info()/warn()/error()/fetal()
3.  Reserve line num and thread name to record the simulate result
'''
import logging
import os
import threading
import time
class Logger(object):
    _instance_lock = threading.Lock()
    __log_instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Logger, "_instance"):
            with Logger._instance_lock:
                if not hasattr(Logger, "_instance"):
                    Logger._instance = object.__new__(cls)
                    logging.basicConfig(level=logging.INFO,
                                        format='%(asctime)s -%(threadName)s - [line:%(lineno)d] - %(levelname)s: %(message)s')
                    Logger.__log_instance = logging.getLogger(__name__)
                    rq = time.strftime('%Y%m%d%H', time.localtime(time.time()))
                    log_name = os.getcwd() + '/' + rq + '.log'
                    try:
                        file = open(log_name, 'r')
                    except:
                        pass
                    else:
                        file.close()
                    logfile = log_name
                    fh = logging.FileHandler(logfile, mode='w')
                    fh.setLevel(logging.INFO)
                    formatter = logging.Formatter(
                        "%(asctime)s -%(threadName)s - [line:%(lineno)d] - %(levelname)s: %(message)s")
                    fh.setFormatter(formatter)
                    Logger.__log_instance.addHandler(fh)
        return Logger._instance

    def do(self):
        return Logger.__log_instance
