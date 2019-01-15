# -*- coding: UTF-8 -*-
import threading
import time
from GlobalSetting import paras
from LogUtils import Logger
from Node import Node


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
    time.sleep(paras.SIMULATOR_TIME + 10)
    Logger().do().info('req :'+str(Node.count_all_req) + ' taken: '+str(Node.count_all_taken))
    Node.count_all_taken = 0
    Node.count_all_req=0


if __name__ == '__main__':

    paras.SIMULATOR_TIME = 60

    paras.REQ_EXP_VALUE = 0.2
    paras.NODE_NUMBER = 32
    asumilation()


