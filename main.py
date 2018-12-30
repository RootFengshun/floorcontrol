# -*- coding: UTF-8 -*-
import threading
import time
from GlobalSetting import paras
from LogUtils import Logger


import NodeManager
import Server

def start_server():
    Server.main()


def start_node_manaager():
    NodeManager.main()
def asumilation():
    Logger().do().info(str(paras.RETRY_OPEN) + ' '+str(paras.NODE_NUMBER)+' '+str(paras.REQ_EXP_VALUE))
    t1 = threading.Thread(target=start_server, name='ServerThread')
    t1.start()
    time.sleep(1)
    t2 = threading.Thread(target=start_node_manaager, name='NodeManagerThread')
    t2.start()
    time.sleep(paras.SIMULATOR_TIME + 5)

if __name__ == '__main__':
    paras.SIMULATOR_TIME = 300
    paras.RETRY_OPEN = False
    paras.REQ_EXP_VALUE=0.1
    paras.NODE_NUMBER = 5
    asumilation()

    paras.REQ_EXP_VALUE=0.1
    paras.NODE_NUMBER = 10
    asumilation()

    paras.REQ_EXP_VALUE = 0.1
    paras.NODE_NUMBER = 20
    asumilation()

    paras.REQ_EXP_VALUE = 0.05
    paras.NODE_NUMBER = 5
    asumilation()

    paras.REQ_EXP_VALUE = 0.05
    paras.NODE_NUMBER = 10
    asumilation()

    paras.REQ_EXP_VALUE = 0.05
    paras.NODE_NUMBER = 20
    asumilation()

    paras.REQ_EXP_VALUE = 0.01
    paras.NODE_NUMBER = 5
    asumilation()

    paras.REQ_EXP_VALUE = 0.01
    paras.NODE_NUMBER = 10
    asumilation()

    paras.REQ_EXP_VALUE = 0.01
    paras.NODE_NUMBER = 20
    asumilation()

    paras.RETRY_OPEN = True

    paras.REQ_EXP_VALUE = 0.1
    paras.NODE_NUMBER = 5
    asumilation()

    paras.REQ_EXP_VALUE = 0.1
    paras.NODE_NUMBER = 10
    asumilation()

    paras.REQ_EXP_VALUE = 0.1
    paras.NODE_NUMBER = 20
    asumilation()

    paras.REQ_EXP_VALUE = 0.05
    paras.NODE_NUMBER = 5
    asumilation()

    paras.REQ_EXP_VALUE = 0.05
    paras.NODE_NUMBER = 10
    asumilation()

    paras.REQ_EXP_VALUE = 0.05
    paras.NODE_NUMBER = 20
    asumilation()

    paras.REQ_EXP_VALUE = 0.01
    paras.NODE_NUMBER = 5
    asumilation()

    paras.REQ_EXP_VALUE = 0.01
    paras.NODE_NUMBER = 10
    asumilation()

    paras.REQ_EXP_VALUE = 0.01
    paras.NODE_NUMBER = 20
    asumilation()





