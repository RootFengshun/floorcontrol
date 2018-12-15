# -*- coding: UTF-8 -*-
import threading
import time
import math

import NodeManager
import Server


def start_server():
    Server.main()


def start_node_manaager():
    NodeManager.main()

def enter():
    global timer
    timer = threading.Timer(5,test)
    timer.start()


def test():
    print time.time()

def cancelthread():
    timer.cancel()



if __name__ == '__main__':
    # print time.time()
    # enter()
    # time.sleep(1)
    # t1 = threading.Thread(target=cancelthread, name='ServerThread')
    # t1.start()
    #
    #
    # enter()



    t1 = threading.Thread(target=start_server, name='ServerThread')
    t1.start()
    time.sleep(2)
    t2 = threading.Thread(target=start_node_manaager, name='NodeManagerThread')
    t2.start()
