# -*- coding: UTF-8 -*-
import threading

from LogUtils import Logger
from Node import Node
from GlobalSetting import paras


def startNodethread(name):
    n = Node(name)


def main():
    Logger().do().info('start node manager')
    for i in range(paras.NODE_NUMBER):
        t = threading.Thread(target=startNodethread, name='LoopThread' + str(i), args=(i,))
        t.start()


if __name__ == '__main__':
    main()
