# -*- coding: UTF-8 -*-
import threading
import time

import NodeManager
import Server


def start_server():
    Server.main()


def start_node_manaager():
    NodeManager.main()


if __name__ == '__main__':
    t1 = threading.Thread(target=start_server, name='ServerThread')
    t1.start()
    time.sleep(2)
    t2 = threading.Thread(target=start_node_manaager, name='NodeManagerThread')
    t2.start()
    print 'main thread done'
