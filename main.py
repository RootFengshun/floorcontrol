# -*- coding: UTF-8 -*-
import threading
import time
from GlobalSetting import paras
from LogUtils import Logger

import UE


def asumilation():
    Logger().do().info(str(paras.RETRY_OPEN) + ' '+str(paras.NODE_NUMBER)+' '+str(paras.REQ_EXP_VALUE))
    UE.main()
    # time.sleep(5)
    # Logger().do().info('req :'+str(Node.count_all_req) + ' taken: '+str(Node.count_all_taken))
    # Node.count_all_taken = 0
    # Node.count_all_req=0


if __name__ == '__main__':

    paras.SIMULATOR_TIME=3600

    paras.RETRY_OPEN = False
    paras.BACKOFF_METHOD = 0

    # paras.NODE_NUMBER = 4
    # asumilation()
    # paras.NODE_NUMBER = 8
    # asumilation()
    # paras.NODE_NUMBER = 16
    # asumilation()
    # paras.NODE_NUMBER = 32
    # asumilation()
    # paras.NODE_NUMBER = 64
    # asumilation()
    # paras.NODE_NUMBER = 128
    # asumilation()
    # paras.NODE_NUMBER = 256
    # asumilation()


    # paras.RETRY_OPEN = True
    # paras.BACKOFF_METHOD = 0
    # paras.NODE_NUMBER = 4
    # asumilation()
    # paras.NODE_NUMBER = 8
    # asumilation()
    # paras.NODE_NUMBER = 16
    # asumilation()
    # paras.NODE_NUMBER = 32
    # asumilation()
    # paras.NODE_NUMBER = 64
    # asumilation()
    # paras.NODE_NUMBER = 128
    # asumilation()
    # paras.NODE_NUMBER = 256
    # asumilation()

    paras.RETRY_OPEN = True
    paras.BACKOFF_METHOD = 1
    paras.NODE_NUMBER = 4
    asumilation()
    paras.NODE_NUMBER = 8
    asumilation()
    paras.NODE_NUMBER = 16
    asumilation()
    paras.NODE_NUMBER = 32
    asumilation()
    paras.NODE_NUMBER = 64
    asumilation()
    paras.NODE_NUMBER = 128
    asumilation()
    paras.NODE_NUMBER = 256
    asumilation()


